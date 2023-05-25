opcode = {"add": ["00000","A"],"sub":["00001","A"],"mov":["0001",""],"ld":["00100","D"],
          "st":["00101","D"],"mul":["00110","A"],"div":["00111","C"],"rs":["01000","B"],
          "ls":["01001","B"],"xor":["01010","A"],"or":["01011","A"],"and":["01100","A"],
          "not":["01101","C"],"cmp":["01110","C"],"jmp":["01111","E"],"jlt":["11100","E"],
          "jgt":["11101","E"],"je":["11111","E"],"hlt":["11110","F"]}

def reg_check(register):
    return bool(register in reg_addr and register != "FLAGS");

def flag_check(register):
    return bool(register == "FLAGS");

def immediate_val_chk(imm):
    if (imm[0] == "$" and imm[1:].isdigit()):
        return (bool(int(imm[1:]) >= 0 and imm[1:] < 256))
    else:
        return False

def var_check(var):
    return (bool(var in var_dict))