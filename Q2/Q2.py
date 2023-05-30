from sys import stdin,stdout,exit
import type_A as A
import type_B as B
import type_C as C
import type_D as D
import type_E as E

PC = 0
mem = ['0'*16] * 256

text = ["1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","1000000000001010","0101000000000000"]

commands = []

for i in range(len(text)):
    text[i] = text[i].strip()
    commands.append(text[i])

commands = list(filter(lambda a: a != "",commands))

Reg_File = {'000' : 0, '001' : 0, '010' : 0, '011' : 0, '100' : 0, '101' : 0, '110' : 0, '111' : 0}

opcode = {"00000": [A.add,"A"],"00001":[A.sub,"A"],"00010":[B.mov_i,"B"],"00100":[D.load,"D"],
		  "00101":[D.store,"D"],"00110":[A.mul,"A"],"00111":[C.div,"C"],"01000":[B.right,"B"],
		  "01001":[B.left,"B"],"01010":[A.xor,"A"],"01011":[A.or_,"A"],"01100":[A.and_,"A"],
		  "01101":[C.not_,"C"],"01110":[C.cmp,"C"],"01111":[E.jmp,"E"],"11100":[E.jlt,"E"],
		  "11101":[E.jgt,"E"],"11111":[E.je,"E"],"11010":["hlt","F"]}

i=0

def mem_allocation():
    for i in range(len(commands)):
        mem[i] = commands[i]
    print(mem)
mem_allocation()

def bin_convert(number,length):
    number = bin(number)[2:]
    number = number.rjust(length,'0')
    return number

def show_mem():
    for line in mem:
        stdout.write(line + '\n')

def output():
    stdout.write(bin_convert(PC,8))
    for reg in Reg_File:
        stdout.write(bin_convert(Reg_File[reg],16))
    stdout.write('\n')

def dec_int(str):
    str=str[::-1]
    result=sum([int(str[i])*(2**i)for i in range(len(str))])
    return result

def exec(line):
    
    prev_flags=bin_convert(Reg_File['111'],16)

    code=line[:5]
    type=opcode[code][1]
    if type == "A":
        line = A(line)
    elif type == "B":
        line = B(line)
    elif type == "C":
        line = C(line)
    elif type == "D":
        line = D(line)
    elif type == "E":
        line = E(line)
    
    curr_flags = bin_convert(Reg_File['111'],16)
    if (curr_flags == prev_flags):
        Reg_File['111']=0

    output()


while mem[PC] != '1101000000000000':
    exec(mem[PC])
    if (j_PC != -1):
        PC = j_PC
        j_PC = -1
    else:
        PC += 1

Reg_File['111']=0
output()
show_mem()