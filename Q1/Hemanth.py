# opcode = {"add": ["00000","A"],"sub":["00001","A"]}
reg_addr = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}
file_read_words=["ls","R1","$12"]


def type_b(opcode,file_read_words):
    reg= reg_addr[file_read_words[1]]
    
    a=file_read_words[2]
    val=int(a[1:])
    imm_bin=bin(val)
    
    return (opcode + "_0_" + reg + "_" + imm_bin)
    

