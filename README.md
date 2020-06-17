# basic-self-checksumming: A basic implementation of self-checksumming for C programs in python
This repository provides a sample solution for `exercise 5.4` of the Security Engineering course (summer term 2020) at the Technical University of Munich. 

The tool comprises two scripts: `protect.py` and `postpatch.py` adhering to the exercise specifications.

# Specifications
SC is one of the most prominent integrity protection techniques. In this exercise, you will implement a simplified (proof-of-concept) self-checksumming protection tool/macro for C/C++ programs. You can use your desired programming/scripting language. We recommend using python. The protect tool gets two inputs: a path to the C/C++ program to protect, and the name of the sensitive function. Make sure your tool can be triggered from the command line with the specified flags.

```./protect -p program.c -f 'function to protect name'```

- Users need to be able to specify one desired function to be protected as a command-line argument
- The protection shall insert a call to a guardMe function in the main function with two arguments:
  - address of the function to protect and 
  - the function’s expected hash value—The expected hash value cannot be known before compilation, use a 1 byte constant integer value as a placeholder
- The guardMe function calculates a 1-byte accumulative XOR hash of the function body (in the code segment) at runtime
- The guardMe function matches the calculated hash with the expected hash value (passed as an argument to the function)
- If the calculated XOR mismatches the expected hash, the guardMe function terminates the program
- A post-patching script shall automatically find the placeholder of the expected hash and set it to the right value based on the function’s XOR—the script shall find the specified function in the binary and calculate a 1-byte XOR of its body. 
- Your script shall accept the following command-line arguments:

```./postpatch.py -b program.out -f 'protected function name' -p placeholder```


# Requirements
- Python 2.7+
- Radare 2 (version 3.5.1+)

  Build and install Radare 2 locally:
  
  ```git clone https://github.com/radareorg/radare2 && cd radare2 && sys/install.sh```
- pip library depndencies: (use ```pip install XXX```)
  - r2pipe 
  - argparse
  - mmap
  - pprint
  
  
# Tool usage
- Clone the respository `git clone https://github.com/mr-ma/basic-self-checksumming`
- Install pip dependencies 
- Protect the `sensitive` function in the sample program (enclosed sample.c):

  ```python protect.py -p sample.c -f sensitive```

- Patch the placeholders in the compiled binary:

  ```python postpatch.py -b out/sample-protected.out -f sensitive -p 222222222 333333333```

*Note:* the protect script uses two hardcoded placeholders (222222222 and 333333333) as placeholders for function size and expected hash, respectively.






