reg_addr = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}
file_read_words=["ls","R1","$12"]


def type_b(opcode,file_read_words):
    reg= reg_addr[file_read_words[1]]
    
    a=file_read_words[2]
    val=int(a[1:])
    imm_bin=bin(val)
    
    return (opcode + "_0_" + reg + "_" + imm_bin)
    

def missing_hlt(file_read_words):
    for i in file_read_words:
        if file_read_words[i] =='hlt':
            a=True
    if a==True:
        pass
    else:
        print("hlt was not found")
        return
        
def var_not_dec(file_read_words,opcode,reg_addr):
    for i in file_read_words:
        if i in opcode or i in reg_addr:
            pass
        else:
            print("variable not declared")
            break
    return

def misuse_label_var(file_read_words,opcode):
    if file_read_words[0][0] == 'j':
        if file_read_words[1][0] == 'l':
            pass
        else:
            print("misuse of labels and variables")
    elif file_read_words[0] in opcode and file_read_words[0][0] != 'j':
        if file_read_words[1] in reg_addr:
            pass
        else:
            print("misuse of labels and variables")
    return