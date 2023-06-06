For Assembler:  (Question 1)
    An assembler is a software tool that converts assembly language source code into machine code, which can be directly executed by a processor.
    In our case, we have developed an assembler using Python. It takes input from a file through standard input (stdin) and converts it into 16-bit binary code. The resulting binary code is saved in an output file called "output.txt" and is also displayed in the terminal.
    Our assembler has a priority handling mechanism, means it handles errors based on priorities given in the error dictionary. This means that if multiple errors exist in a program, only the first error encountered from the dictionary will be displayed and the program will come to a halt.


For Simulator: (Question 2)
    We have developed the simulator using Python. It takes input through standard input (stdin) and stores it in list named mem which has elements of 16 bit binary code in the form of '0000000000000000' initially.
    The registers are stored in dictionary named Reg_File with register names as key which stores values of registers. The Flag register stores a string.
    The simulator reads binary machine code from the standard console. The instructions are then stored in the memory. Instructions are then executed line by line until the machine code equivalent of `hlt` is reached.
    When the `hlt` statement is read, the entire state of the program's memory is printed out on the console.
    This is the output of the simulator.
