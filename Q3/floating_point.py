def bin_to_float(binary):
    exp = binary[:3]
    mantissa = binary[3:]
    res = 2**(int(exp,2)) * (1 + int(mantissa,2)/2**5)
    return res

def float_check(f: str) -> bool:
    if (f[0] == "$"):
        return True
    else:
        return False