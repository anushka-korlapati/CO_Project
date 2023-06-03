from sys import stdin,stdout,exit

text = stdin.readlines()
# print(text)
commands = []
for i in range(len(text)):
    text[i] = text[i].strip()
    commands.append(text[i])
# with open("HardGen/test02.txt") as inline:
#     txt = inline.readlines()
#     commands = [txt[i].strip() for i in range(len(txt))]
# print(commands)
commands = list(filter(lambda a: a != "", commands))
# print(commands)
L = []

#Op code Dictionary with format {operation : [opcode, type]} 
opcode = {"add": ["00000","A"],"sub":["00001","A"],"mov":["0001",""],"ld":["00100","D"],
		  "st":["00101","D"],"mul":["00110","A"],"div":["00111","C"],"rs":["01000","B"],
		  "ls":["01001","B"],"xor":["01010","A"],"or":["01011","A"],"and":["01100","A"],
		  "not":["01101","C"],"cmp":["01110","C"],"jmp":["01111","E"],"jlt":["11100","E"],
		  "jgt":["11101","E"],"je":["11111","E"],"hlt":["11010","F"],"addf":["10000","A"],
          "subf":["10001","A"],"movf":["10010","B"]}

#registery dictionary with format {register : regcode}
reg_addr = {"R0":"000", "R1":"001", "R2":"010",
            "R3":"011", "R4":"100", "R5":"101",
            "R6":"110", "FLAGS":"111"}

#error dict
error = {"1" : "Multiple hlt statements", "2" : "last instruction is not hlt",
         "3" : "Register not found", "4" : "Illegal use of flags register", "5" : "Variable not defined",
         "6" : "variable not defined at start", "7" : "label not found",
         "8" : "Duplicate variable", "9" : "Duplicate label", "10" : "Invalid Syntax",
         "11" : "No hlt instruction found", "12" : "Variable used as label", "13" : "Label used as variable",
         "14" : "Immediate value not found", "15" : "Invalid operation", "16": "Flaoting Point Number exceeds 8 bit"}

#exits the program while showing the line at which error is caused
def errors(code: str, line: str = "-1") -> None:
    if (line == "-1"):
        # print(error[code] + "\nAssembly Halted")
        stdout.write(error[code] + "\nAssembly Halted\n")
        stdout.close()
        exit()
    # print("Error at line " + line + ", " + error[code] + "\nAssembly Halted")
    stdout.write("Error at line " + line + ", " + error[code] + "\nAssembly Halted\n")
    stdout.close()
    exit()

#making dictionaries for variables, labels, opcodes
def parsing(data: list[str]) -> tuple[dict[str,str], dict[str,str], dict[str,list[str]]]:
    var_dict,label_dict,op_dict = {},{},{}
    data = [line.split() for line in data]
    lin = len(data)
    var_start = True
    for i in range(lin):
        ln = data[i]
        #checks if variable is in the start and if variable is legally identified
        if ln[0] == "var":
            if len(ln) != 2:
                # print(1)
                errors("10", str(i + 1))
            if not var_start:
                errors("6", str(i + 1))
            if ln[1] in var_dict:
                errors("8", str(i + 1))
            var_dict[ln[1]] = lin
            lin += 1
        #checks for a colon in the line, if present then check conditions for label and stores in label_dict
        elif ": " in " ".join(ln):
            if ln[0][-1] != ":":
                # print(1)
                errors("10", str(i + 1))
            if ln[0][:-1] in label_dict:
                errors("9", str(i + 1))
            label_dict[ln[0][:-1]] = i
            ln = ln[1:]
            if ln[0] in opcode:
                op_dict[str(i)] = ln
            else:
                errors("10", str(i + 1))
            var_start = False
        elif ln[0] in opcode:
            op_dict[str(i)] = ln
            var_start = False
        else:
            errors("15", str(i + 1))
    #checking if the last operation is hlt and also checking for multiple hlt statements
    # print(op_dict)
    hlt_counter = 0
    for values in op_dict.values():
        if values[0] == "hlt":
            hlt_counter += 1
    # print(list(op_dict.values())[-1])
    if hlt_counter == 0:
        errors("11")
    elif hlt_counter > 1:
        errors("1", str(commands.index(["hlt"]) + 1))
    if (commands[-1][0] != "hlt" and ["hlt"] in commands):
        errors("2",str(commands.index(["hlt"]) + 1))

    offset = len(var_dict)
    var_dict = {key : bin(var_dict[key] - offset)[2:].rjust(7, '0')
                for key in var_dict}
    label_dict = {key : bin(label_dict[key] - offset)[2:].rjust(7, '0')
                for key in label_dict}
    op_dict = {str(int(key) - offset) : op_dict[key]
                for key in op_dict}
    return var_dict,label_dict,op_dict

def Type_A(file_read_words: list[str]) -> str:
    return "00" + reg_addr[file_read_words[1]] + reg_addr[file_read_words[2]] + reg_addr[file_read_words[3]]

def Type_B(file_read_words: list[str], imm: str) -> str:
    return "0" + reg_addr[file_read_words[1]] + bin(int(imm))[2:].rjust(7,'0')

def Type_C(file_read_words: list[str]) -> str: 
    return "00000" + reg_addr[file_read_words[1]] + reg_addr[file_read_words[2]]

def Type_D(file_read_words: list[str], memaddr: str, var_dict: dict[str,str]) -> str:
    return "0" + reg_addr[file_read_words[1]] + var_dict[memaddr]

def Type_E(memaddr: str, label_dict: dict[str,str]) -> str:
    return "0000" + label_dict[memaddr[1]]

def floating_to_bin(num: str, line: str) -> str:
    str_ = num
    find_point = str_.rfind('.')
    lhs = int(str_[:find_point])
    # print(lhs)
    lhs_binary = bin(lhs)[2:]
    # print(lhs_binary)
    rhs = ("0"+(str_[find_point:]))

    l=[]
    i = 0
    while rhs != '0.0':
        # print(1)
        x = float(rhs)*2
        if x<1:
            l.append("0")
        else:
            l.append("1")
        rhs = "0." + str(x).split(".")[1]
        if (i == 8):
            break
        i += 1
    rhs_binary = ""
    for j in l:
        rhs_binary += (j)
    if (len(rhs_binary) != 5):
        while (len(rhs_binary) != 5):
            rhs_binary += "0"
    lhs_binary.rjust(3,"0")
    final_bin = lhs_binary + rhs_binary
    if (len(final_bin) > 8):
        errors("16", line)
    return final_bin

def Type_Floating(file_read_words: list[str], imm: str, line: str) -> str:
    return reg_addr[file_read_words[1]] + floating_to_bin(imm, line)

def hlt() -> str:
    return "00000000000"

#checking if the register value is in the reg_dict
def reg_check(register: str) -> bool:
    return bool(register in reg_addr and register != "FLAGS")

def flag_check(register: str) -> bool:
    return bool(register == "FLAGS")

def immediate_val_chk(imm: str) -> bool:
    if (imm[0] == "$" and imm[1:].isdigit()):
        return (bool(int(imm[1:]) >= 0 and int(imm[1:]) < 256))
    else:
        return False

def var_check(var: str, var_dict: dict[str,str]) -> bool:
    return (bool(var in var_dict))

def label_check(lbl: str, label_dict: dict[str,str]) -> bool:
    return bool(lbl in label_dict)

def main_process(var_dict: dict[str, str], label_dict: dict[str, str], op_dict: dict[str, str]) -> None:
    # print(op_dict)
    for num in op_dict:
        # print(op_dict[num])
        ln = op_dict[num]
        operation = ln[0]
        op = opcode[operation][0]
        op_type = opcode[operation][1]
        if op == "0001":
            if (len(ln) != 3):
                errors("10", str(int(num) + 1))
            elif not reg_check(ln[1]):
                errors("3", str(int(num) + 1))
            if (immediate_val_chk(ln[2])):
                op += "0"
                op_type = "B"
                L.append(op + Type_B(ln, ln[2][1:]))
            elif reg_check(ln[2]) or flag_check(ln[2]):
                op += "1"
                op_type = "C"
                L.append(op + Type_C(ln))
            else:
                errors("10", str(int(num) + 1))
        else:
            if op_type == "A":
                if len(ln) != 4:
                    # print(2)
                    errors("10", str(int(num) + 1))
                elif not (reg_check(ln[1]) and reg_check(ln[2]) and reg_check(ln[3])):
                    if (flag_check(ln[1]) or flag_check(ln[2]) or flag_check(ln[3])):
                        errors("4", str(int(num) + 1))
                    errors("10", str(int(num) + 1))
                else:
                    L.append(op + Type_A(ln))
            elif op_type == "B":
                if len(ln) != 3:
                    # print(2)
                    errors("10", str(int(num) + 1))
                elif not reg_check(ln[1]):
                    if flag_check(ln[1]):
                        errors("4", str(int(num) + 1))
                    errors("10", str(int(num) + 1))
                elif ("." in ln[2][1:]):
                    L.append(op + Type_Floating(ln, ln[2][1:], str(int(num) + 1)))
                elif not immediate_val_chk(ln[2]):
                    errors("14", str(int(num) + 1))
                else:
                    L.append(op + Type_B(ln, ln[2]))
            elif op_type == "C":
                if len(ln) != 3:
                    # print(2)
                    errors("10", str(int(num) + 1))
                if not (reg_check(ln[1]) and reg_check(ln[2])):
                    errors("3", str(int(num) + 1))
                L.append(op + Type_C(ln))
            elif op_type == "D":
                if len(ln) != 3:
                    # print(2)
                    errors("10", str(int(num) + 1))
                if not (reg_check(ln[1])):
                    if flag_check(ln[1]):
                        errors("4", str(int(num) + 1))
                    errors("10", str(int(num) + 1))
                if not var_check(ln[2], var_dict):
                    if label_check(ln[2], label_dict):
                        errors("12", str(int(num) + 1))
                    errors("5", str(int(num) + 1))
                L.append(op + Type_D(ln,ln[2],var_dict))
            elif op_type == "E":
                if len(ln) != 2:
                    # print(2)
                    errors("10", str(int(num) + 1))
                if not label_check(ln[1], label_dict):
                    if var_check(ln[1], var_dict):
                        errors("13", str(int(num) + 1))
                    errors("7", str(int(num) + 1))
                L.append(op + Type_E(ln,label_dict))
            else:
                if ln != ['hlt']:
                    errors("10", str(int(num) + 1))
                L.append(op + hlt())

def main():
    # print(commands)
    var_dict,label_dict,op_dict = parsing(commands)
    main_process(var_dict, label_dict, op_dict)
    for i in range(len(L)):
        stdout.write(L[i] + "\n")
    stdout.close()

main()