opcode = {"add": ["00000","A"],"sub":["00001","A"],"mov":["0001",""],"ld":["00100","D"],
		"st":["00101","D"],"mul":["00110","A"],"div":["00111","C"],"rs":["01000","B"],
		"ls":["01001","B"],"xor":["01010","A"],"or":["01011","A"],"and":["01100","A"],
		"not":["01101","C"],"cmp":["01110","C"],"jmp":["01111","E"],"jlt":["11100","E"],
		"jgt":["11101","E"],"je":["11111","E"],"hlt":["11110","F"]}

reg_addr = {"R0":"000", "R1":"001", "R2":"010",
		"R3":"011", "R4":"100", "R5":"101",
		"R6":"110", "FLAGS":"111"}

def Type_A(file_read_words):
    return "00" + reg_addr[file_read_words[1]] + reg_addr[file_read_words[2]] + reg_addr[file_read_words[3]]

def Type_B(file_read_words):
    return "0" + reg_addr[file_read_words[1]] + bin(int(file_read_words[2])[2:]).rjust(8,'0')

def Type_C(file_read_words):
    return "00000" + reg_addr[file_read_words[1]] + reg_addr[file_read_words[2]]

def Type_D(file_read_words, memaddr):
    return "0" + reg_addr[file_read_words[1]] + memaddr

def Type_E(memaddr):
    return "0000" + memaddr

def Type_F():
    return "00000000000"