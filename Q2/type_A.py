class A:
    def __init__(self, out):
        self.reg1 = out[7:10]
        self.reg2 = out[10:13]
        self.reg3 = out[13.16]
        self.op = opcode[out[:5]]