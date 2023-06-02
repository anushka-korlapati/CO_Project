def floating_to_bin(num: float) -> str:
    str_ = str(num)

    find_point = str_.rfind('.')
    lhs = int(str_[:find_point])
    print(lhs)
    lhs_binary = bin(lhs)[2:]
    print(lhs_binary)
    rhs = ("0"+(str_[find_point:]))

    l=[]
    while rhs != '0.0':
        # print(1)
        x = float(rhs)*2
        if x<1:
            l.append("0")
        else:
            l.append("1")
        rhs = "0." + str(x).split(".")[1]
        print(rhs)
    rhs_binary = ""
    for j in l:
        rhs_binary += (j)
    return lhs_binary + "." + rhs_binary

def bin_to_floating(num: str) -> int:
    lhs, rhs = num.split(".")
    lhs_int = 0
    rhs_int = 0
    j = len(lhs) - 1
    for i in range(len(lhs)):
        lhs_int += int(lhs[j]) * 2**i
        j -= 1
    for i in range(1,len(rhs) + 1):
        rhs_int += int(rhs[i - 1]) * 2**(-i)
    
    floating_number = lhs_int + rhs_int
    return floating_number


print(floating_to_bin(58.293))
