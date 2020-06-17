import argparse
import os
import r2pipe
import struct
import mmap
import base64
from shutil import copyfile
import pprint
pp = pprint.PrettyPrinter(indent=4)


def precompute_hash(r2, offset, size):
    print('Precomputing hash')
    h = 0
    print("r2 command to get the function body in base64:\np6e {}@{}".format(size, offset))
    b64_func = r2.cmd("p6e {}@{}".format(size, offset))
    func_bytes = bytearray(base64.b64decode(b64_func))
    for b in func_bytes:
        h = h ^ b
    print('Precomuted hash:', hex(h))
    return h


def patch_binary(mm, search_value, patch_value):
    print("search value:{} patch value:{}".format(search_value, patch_value))
    flag = "<I"  # little-endian unsigned int
    search_bytes = struct.pack(flag, search_value)
    address = mm.find(search_bytes)
    if address == -1:
        mm.seek(0)
        address = mm.find(search_bytes)
    mm.seek(address, os.SEEK_SET)
    patch_bytes = struct.pack(flag, patch_value)
    mm.write(patch_bytes)


def get_protected_function_info(r2, function):
    # find addresses and sizes of all functions
    r2.cmd("aa")
    r2.cmd("aac")
    function_list = r2.cmdj("aflj")
    # print(function_list)
    funcs = {}
    for func in function_list:
        attr = {'size': func['size'], 'offset': func['offset']}
        funcs[func['name']] = attr

    # Basic search for mangled names
    if function == 'main':
        # main function is entry0 in the binary
        function = 'entry0'
        print("Cannot precompute the expected hash for the main function, why is that?")
        exit(1)
    match = 0
    mangledName = ""
    for name, attr in funcs.items():
        # sometimes r2 prepends sym. to function names
        if function in name:
            mangledName = name
            match += 1
    if match != 1:
        print("Failed to safely find function in the binary!")
        pp.pprint(funcs)
        exit(1)
    return funcs[mangledName]


def main():
    parser = argparse.ArgumentParser(
        description='Postpatch protected C program.')
    parser.add_argument('-b', action="store", dest="binary",
                        help="program.out protected program binary", required=True)
    parser.add_argument('-f', action="store", dest="function",
                        help="protected function name", required=True)
    parser.add_argument('-p', nargs="+", dest="placeholders",
                        help="list of used placeholders in the exact order of function, size, expected hash", required=True)
    results = parser.parse_args()
    print("python protect program", results)
    r2 = r2pipe.open(results.binary)
    funcInfo = get_protected_function_info(r2, results.function)
    funcOffset = funcInfo["offset"]
    funcSize = funcInfo["size"]
    funcExpectedHash = precompute_hash(r2, funcOffset, funcSize)

    print("funcOffset:{} funcSize:{} funcExpectedHash:{}".format(
        funcOffset, funcSize, funcExpectedHash))
    binaryFile, _ = os.path.splitext(results.binary)
    patchedBinary = "{}-patched.out".format(binaryFile)
    copyfile(results.binary, patchedBinary)
    with open(patchedBinary, 'r+b') as binary:
        mm = mmap.mmap(binary.fileno(), 0)
        patch_binary(mm, int(results.placeholders[0]), int(funcSize))
        patch_binary(mm, int(results.placeholders[1]), int(funcExpectedHash))
    print("Successfully stored patched binary {}".format(patchedBinary))
    status = os.system(
        "chmod +x {}".format(patchedBinary))
    if status != 0:
        print("Error in setting permission, try:\n sudo chmod +x {}".format(patchedBinary))
        exit(1)


if __name__ == '__main__':
    main()
