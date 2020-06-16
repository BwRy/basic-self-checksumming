import argparse
import os


def read_file(program):
    if os.path.exists(program) != True:
        print('File does not exist.')
        return None, True

    f = open(program, "r")
    contents = f.readlines()
    f.close()
    return contents, False


def inject_guard(program, contents, function, insertIndex, outDir):
    filename, extension = os.path.splitext(program)
    protectedProgram = "{}/{}-protected{}".format(outDir, filename, extension)
    outfile = open(protectedProgram, 'w')
    outfile.write("#include \"../protect.hpp\"\n")
    for i, line in enumerate(contents):
        outfile.write(line)
        # insertIndex+1 to skip the curly brace of the main body
        if i == insertIndex+1:
            outfile.write(
                '\tguardMe({},222222222,333333333);\n'.format(function))
    outfile.close()
    print("Created protected file: {}".format(protectedProgram))
    return protectedProgram


def process_file(program, function, outDir):
    programlines, err = read_file(program)
    if err:
        exit(1)
    insertindex = -1
    for i in range(len(programlines)):
        if 'int main()' in programlines[i]:
            insertindex = i
            break
    if insertindex != -1:
        # insert guardcall
        return inject_guard(program, programlines, function, insertindex, outDir)
    else:
        print('Failed to find main function')


def compile_file(protectedProgram):
    filename, _ = os.path.splitext(protectedProgram)
    binary = "{}.out".format(filename)
    status = os.system(
        "gcc {} -o {}".format(protectedProgram, binary))
    if status != 0:
        print("Error in compilation")
        exit(1)
    else:
        print("Successfully compiled binary: {}".format(binary))


def main():
    parser = argparse.ArgumentParser(description='Protect input C program.')
    parser.add_argument('-p', action="store", dest="program",
                        help="program.c to protect", required=True)
    parser.add_argument('-f', action="store", dest="function",
                        help="function to protect name", required=True)
    results = parser.parse_args()
    print("python protect program", results)
    outDir = 'out'
    status = os.system(
        "mkdir -p {}".format(outDir))
    if status != 0:
        print("Error in creating '{}' directory".format(outDir))
        exit(1)
    protectedProgram = process_file(results.program, results.function, outDir)
    compile_file(protectedProgram)


if __name__ == '__main__':
    main()
