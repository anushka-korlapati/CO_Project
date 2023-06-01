from sys import stdin,stdout

#Program Counter
PC = 0
mem = ['0'*16] * 256

overflow = 2**16 - 1
underflow = 0
jump = -1

# text = ["0000000000001010","0000000000001010","0000000000001010","0000000000001010","0000000000001010","1101000000000000"]
# text = ["0001000100001010",
# "0001001001100100",
# "0011000011001010",
# "0010101100000101",
# "1101000000000000",
# ]
# commands = []
# text = stdin.readlines()
# for i in range(len(text)):
#     text[i] = text[i].strip()
#     commands.append(text[i])

with open("bin/hard/test1") as inline:
    txt = inline.readlines()
    commands = [txt[i].strip() for i in range(len(txt))]
commands = list(filter(lambda a: a != "",commands))

Reg_File = {'000' : 0, '001' : 0, '010' : 0, '011' : 0, '100' : 0, '101' : 0, '110' : 0, '111' : 0}

def mem_store():
    for i in range(len(commands)):
        mem[i] = commands[i]
    # print(mem)
mem_store()

def line_output() -> None:
    stdout.write(f"{dec_to_bin(PC,7)} ")
    for register in Reg_File:
        stdout.write(f"{dec_to_bin(Reg_File[register],16)} ")
    stdout.write("\n")

def bin_to_dec(string: str) -> int:
    result = 0
    j = 0
    for i in range(len(string) - 1, -1,-1):
        result += int(string[i]) * 2**j
        j += 1
    return result

def dec_to_bin(string: int, lenght: int) -> str:
    string = bin(string)[2:]
    string = string.rjust(lenght, "0")
    return string

#Type A
def add(r1: str,r2: str,r3: str) -> None:
    result = Reg_File[r1] + Reg_File[r2]
    if result > overflow:
        Reg_File['111'] += 8
        result = result % (overflow + 1)
    Reg_File[r3] = result

def sub(r1: str,r2: str,r3: str):
    result = Reg_File[r1] - Reg_File[r2]
    if result < underflow:
        Reg_File['111'] += 8
        result = 0
    Reg_File[r3] = result

def mul(r1: str,r2: str,r3: str):
    result = Reg_File[r1] * Reg_File[r2]
    if result > overflow:
        Reg_File['111'] += 8
        result = result % (overflow + 1)
    Reg_File[r3] = result

def xor(r1: str,r2: str,r3: str):
    Reg_File[r3] = Reg_File[r1] ^ Reg_File[r2]

def or_(r1: str,r2: str,r3: str):
    Reg_File[r3] = Reg_File[r1] | Reg_File[r2]

def and_(r1: str,r2: str,r3: str):
    Reg_File[r3] = Reg_File[r1] & Reg_File[r2]

#Type B
def mov_i(reg: str,imm: str):
    Reg_File[reg] = bin_to_dec(imm)

def right(reg: str,imm: str):
    result = Reg_File[reg] >> imm
    if result > overflow:
        result = result % (overflow + 1)
    Reg_File[reg] = result

def left(reg: str,imm: str) -> None:
    Reg_File[reg] = Reg_File[reg] << imm

#Type C
def mov_r(line: str):
    Reg_File[line[13:16]] = Reg_File[line[10:13]]

def div(line: str):
    Reg_File['000'] = Reg_File[line[10:13]] / Reg_File[line[13:16]]
    Reg_File['001'] = Reg_File[line[10:13]] % Reg_File[line[13:16]]

def bit_not(line: str):
    Reg_File[line[10:13]] = overflow + 1 + ~Reg_File[line[13:16]]

def compare(line: str):
    ineq = Reg_File[line[10:13]] > Reg_File[line[13:16]]
    eq = Reg_File[line[10:13]] == Reg_File[line[13:16]]
    if (ineq):
        Reg_File['111'] += 2
    elif (eq):
        Reg_File['111'] += 1
    else:
        Reg_File['111'] += 4

#Type D
def load(line: list[str]):
    Reg_File[line[5:9]] = bin_to_dec(line[9:16])

def store(line: list[str]):
    # print(dec_to_bin(Reg_File[(bin_to_dec(line[6:9]))],16))
    mem[bin_to_dec(line[9:16])] = dec_to_bin(Reg_File[line[6:9]], 16)

#Type E
def unconditional_jump(line):
    global PC
    global jump

    jump = line[9:16]

def equal(line):
    if (Reg_File['111'] % 2 == 1):
        unconditional_jump(line)

def greater(line):
    if ((Reg_File['111'] >> 2) % 2 == 1):
        unconditional_jump(line)

def smaller(line):
    if ((Reg_File['111'] >> 1) % 2 == 1):
        unconditional_jump(line)

opcode = {"00000": [add,"A"],"00001":[sub,"A"],"00010":[mov_i,"B"],'00011':[mov_r,'C'],"00100":[load,"D"],
          "00101":[store,"D"],"00110":[mul,"A"],"00111":[div,"C"],"01000":[right,"B"],
		  "01001":[left,"B"],"01010":[xor,"A"],"01011":[or_,"A"],"01100":[and_,"A"],
		  "01101":[bit_not,"C"],"01110":[compare,"C"],"01111":[unconditional_jump,"E"],"11100":[smaller,"E"],
		  "11101":[greater,"E"],"11111":[equal,"E"],"11010":["hlt","F"]}

def execution(line):
    flag = dec_to_bin(Reg_File["111"],16)

    code = line[:5]
    type = opcode[code][1]
    if (type == "A"):
        # print("1")
        line = opcode[code][0](line[7:10], line[10:13], line[13:16])
    elif (type == "B"):
        # print("2")
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

    if (flag == post_flag):
        Reg_File['111'] = 0
    line_output()


while mem[PC] != "1101000000000000":
    execution(mem[PC])
    # print(Reg_File["000"],Reg_File["001"],Reg_File["010"],Reg_File["011"],Reg_File["100"],Reg_File["101"],Reg_File["110"],Reg_File["111"])
    if (jump==-1):
        PC += 1
    else:
        PC=jump
        jump=-1

line_output()