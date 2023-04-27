reg_addr = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}

#Type C
count = 0
def R_counter():
    for i in file_read_words:
        if i[0] == "R":
            count += 1
    return count
count = R_counter()

def Type_c(opcodes,reg_addr):
    binary = opcodes + '00000'
    for i in file_read_words:
        temp_reg = ''
        if i[0] == "R":
            temp_reg = reg_addr[i]
        binary += temp_reg
    return binary