reg_addr = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}

#Type C
count = 0
def R_counter(file_read_words):
    for i in file_read_words:
        if i[0] == "R":
            count += 1
    return count
count = R_counter()

def Type_c(opcodes,file_read_words):
    binary = opcodes + '00000'
    for i in file_read_words:
        temp_reg = ''
        if i[0] == "R":
            temp_reg = reg_addr[i]
        binary += temp_reg
    return binary


def isa_reg_name_error(file_read_words):
    if file_read_words[0] not in ['add','sub','mov','ld','st','mul','div','rs','ls','xor','or','and','not','cmp','jmp','jlt','jgt','je','hlt']:
        print("Error: Incorrect ISA")
    length = len(file_read_words)
    for i in range(1,length-1):
        if file_read_words[i] not in ['R0','R1',"R2","R3","R4","R5","R6","$Imm","mem_addr"]:
            print("Error: reg name not found")
            break
    return