reg_addr = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}

#Type C


def isa_reg_name_error(file_read_words):
    if file_read_words[0] not in ['add','sub','mov','ld','st','mul','div','rs','ls','xor','or','and','not','cmp','jmp','jlt','jgt','je','hlt','var']:
        print("Error: Incorrect ISA")
    length = len(file_read_words)
    for i in range(1,length-1):
        if file_read_words[i] not in ['R0','R1',"R2","R3","R4","R5","R6","$Imm","mem_addr"]:
            print("Error: reg name not found")
            break
    return

def lable_name_error(file_read_words):
    if file_read_words[0][-1] == ':' and file_read_words[0][-2].isalnum():
        pass
    else:
        print("Invaalid lable")
        return
    
def hlt_last(file_read_words):
    if file_read_words[-1] != 'hlt':
        print("hlt not found at last")
    return