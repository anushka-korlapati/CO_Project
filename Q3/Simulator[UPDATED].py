from sys import stdin,stdout

#Program Counter
PC = 0
#Here it is defining a list(array) where the max number of 
mem = ['0'*16] * 128

#Setting an overflow limit (Basically applying the formula)
overflow = 2**16 - 1
#Underflow limit being set to 0
underflow = 0
#Jump variabl, this comes in action when we have jump operations
jump = -1

#This block of code is for terminal inputs
commands = []
text = stdin.readlines()
for i in range(len(text)):
    text[i] = text[i].strip()
    commands.append(text[i])

#This block of code is for file inputs
# with open("bin/hard/test1") as inline:
#     txt = inline.readlines()
#     commands = [txt[i].strip() for i in range(len(txt))]
# commands = list(filter(lambda a: a != "",commands))

#The final value in integer will be stored which will then convert to binary and be printed
Reg_File = {'000' : 0, '001' : 0, '010' : 0, '011' : 0, '100' : 0, '101' : 0, '110' : 0, '111' : 0}

Var_dict = dict()

#Just copying the inputs to the list defined above
for i in range(len(commands)):
    mem[i] = commands[i]
# print(mem)

#it defines itself that is it prints outputs of every line
def line_output() -> None:
    stdout.write(f"{dec_to_bin(PC,7)}        ")
    for register in Reg_File:
        # print(Reg_File[register])
        stdout.write(f"{dec_to_bin(Reg_File[register],16)} ")
    stdout.write("\n")

def bin_to_floating(binary: str) -> float:
    # Check for special cases: 0, positive/negative infinity, and NaN
    if binary == '00000000':
        return 0.0
    elif binary == '01111000':
        return float('inf')
    elif binary == '11111000':
        return float('-inf')
    elif binary == '11111001':
        return float('nan')

    # Extract the sign, exponent, and mantissa bits
    exponent_bits = binary[0:3]
    mantissa_bits = binary[3:]

    # Calculate the bias for the exponent
    bias = 2**(3 - 1) - 1

    # Convert the exponent from binary to decimal
    exponent = int(exponent_bits, 2) - bias

    # Calculate the implicit leading 1 for the mantissa
    implicit_leading = 1.0

    # Convert the mantissa from binary to decimal
    mantissa = 0.0
    for i in range(len(mantissa_bits)):
        bit = int(mantissa_bits[i])
        mantissa += bit * (2**(-i - 1))

    # Combine the sign, exponent, and mantissa to get the final floating-point number
    result = implicit_leading * (1 + mantissa) * (2 ** exponent)

    return result

#converts binary to decimal
def bin_to_dec(string: str) -> int:
    result = 0
    j = 0
    for i in range(len(string) - 1, -1,-1):
        result += int(string[i]) * 2**j
        j += 1
    return result

#converts decimal to binary
def dec_to_bin(string: int, lenght: int = 16) -> str:
    string = bin(string)[2:]
    string = string.rjust(lenght, "0")
    return string

#Type A
def add(r1: str,r2: str,r3: str) -> None:
    # print(r1,r2,r3)
    result = Reg_File[r3] + Reg_File[r2]
    if result > overflow:
        Reg_File['111'] += 8
        result = result % (overflow + 1)
    Reg_File[r1] = result

def sub(r1: str,r2: str,r3: str) -> None:
    result = Reg_File[r2] - Reg_File[r3]
    if result < underflow:
        Reg_File['111'] += 8
        result = 0
    Reg_File[r1] = result

def mul(r1: str,r2: str,r3: str) -> None:
    result = Reg_File[r1] * Reg_File[r2]
    if result > overflow:
        Reg_File['111'] += 8
        result = result % (overflow + 1)
    Reg_File[r3] = result

def xor(r1: str,r2: str,r3: str) -> None:
    Reg_File[r3] = Reg_File[r1] ^ Reg_File[r2]

def or_(r1: str,r2: str,r3: str) -> None:
    Reg_File[r3] = Reg_File[r1] | Reg_File[r2]

def and_(r1: str,r2: str,r3: str) -> None:
    Reg_File[r3] = Reg_File[r1] & Reg_File[r2]

#Type B
def mov_i(reg: str,imm: str) -> None:
    Reg_File[reg] = bin_to_dec(imm)

def right(reg: str,imm: str) -> None:
    result = Reg_File[reg] >> imm
    if result > overflow:
        result = result % (overflow + 1)
    Reg_File[reg] = result

def left(reg: str,imm: str) -> None:
    Reg_File[reg] = Reg_File[reg] << imm

def mov_f(reg: str,imm: str) -> None:
    Reg_File[reg] = bin_to_floating(imm)

#Type C
def mov_r(line: str) -> None:
    Reg_File[line[10:13]] = Reg_File[line[13:16]]

def div(line: str) -> None:
    Reg_File['000'] = Reg_File[line[10:13]] / Reg_File[line[13:16]]
    Reg_File['001'] = Reg_File[line[10:13]] % Reg_File[line[13:16]]

def bit_not(line: str) -> None:
    Reg_File[line[10:13]] = overflow + 1 + ~Reg_File[line[13:16]]

def compare(line: str) -> None:
    ineq = Reg_File[line[10:13]] > Reg_File[line[13:16]]
    eq = Reg_File[line[10:13]] == Reg_File[line[13:16]]
    if (ineq):
        Reg_File['111'] += 2
    elif (eq):
        Reg_File['111'] += 1
    else:
        Reg_File['111'] += 4

#Type D
def load(line: str) -> None:
    if (line[9:16] in Var_dict):
        Reg_File[line[6:9]] = bin_to_dec(line[9:16])

def store(line: str) -> None:
    # print(dec_to_bin(Reg_File[(bin_to_dec(line[6:9]))],16))
    mem[bin_to_dec(line[9:16])] = dec_to_bin(Reg_File[line[6:9]], 16)
    Var_dict[line[9:16]] = dec_to_bin(Reg_File[line[6:9]], 16)

#Type E
def unconditional_jump(line) -> None:
    global PC
    global jump

    jump = line[9:16]

def equal(line) -> None:
    if (Reg_File['111'] == 1):
        unconditional_jump(line)

def greater(line) -> None:
    if ((Reg_File['111']) == 2):
        unconditional_jump(line)

def smaller(line) -> None:
    if (Reg_File['111'] == 4):
        unconditional_jump(line)

#this is new opcode that we creating and we have added the functions next to the respective opcode
opcode = {"00000": [add,"A"],"00001":[sub,"A"],"00010":[mov_i,"B"],'00011':[mov_r,'C'],"00100":[load,"D"],
          "00101":[store,"D"],"00110":[mul,"A"],"00111":[div,"C"],"01000":[right,"B"],
		  "01001":[left,"B"],"01010":[xor,"A"],"01011":[or_,"A"],"01100":[and_,"A"],
		  "01101":[bit_not,"C"],"01110":[compare,"C"],"01111":[unconditional_jump,"E"],"11100":[smaller,"E"],
		  "11101":[greater,"E"],"11111":[equal,"E"],"11010":["hlt","F"],"10000":[add,"A"],
          "10001":[sub,"A"],"10010":[mov_f,"B"]}

#here execution is done after splitting the line
def execution(line: str) -> None:
    pre_flag = dec_to_bin(Reg_File["111"],16)

    code = line[:5]
    type = opcode[code][1]
    if (type == "A"):
        # print("1")
        line = opcode[code][0](line[7:10], line[10:13], line[13:16])
    elif (type == "B"):
        # print("2")
        if (code == "10010"):
            line = opcode[code][0](line[5:8], line[8:16])
        line = opcode[code][0](line[6:9], line[9:16])
    elif (type == "C"):
        # print("3")
        line = opcode[code][0](line)
    elif (type == "D"):
        # print("4")
        line = opcode[code][0](line)
    elif (type == "E"):
        # print("5")
        line = opcode[code][0](line)

    post_flag = dec_to_bin(Reg_File["111"],16)

    if (pre_flag == post_flag):
        Reg_File['111'] = 0
    line_output()


while mem[PC] != "1101000000000000":
    execution(mem[PC])
    # print(Reg_File["000"],Reg_File["001"],Reg_File["010"],Reg_File["011"],Reg_File["100"],Reg_File["101"],Reg_File["110"],Reg_File["111"])
    if (jump==-1):
        PC += 1
    else:
        PC=bin_to_dec(jump)
        jump=-1
    # print(Reg_File['011'])

line_output()
for i in range(len(mem)):
    stdout.write(mem[i] + "\n")