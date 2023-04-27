reg_addr = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}
syntax="add R1 R2 R3"
file_read_words=["add","R1","R2","R3"]



def typeA(opcode,file_read_words):

    unused="00"

    reg1=reg_addr[file_read_words[1]]
    reg2=reg_addr[file_read_words[2]]
    reg3=reg_addr[file_read_words[3]]


    binary="00000"+"_"+unused+"_"+reg1+"_"+reg2+"_"+reg3


def typeE(opcode,file_read_words,mem_addr):

    unused="0000"

    binary=opcode+"_"+unused+"_"+mem_addr 

def typeF(opcode):

    unused="00000000000"

    binary=opcode+"_"+unused
