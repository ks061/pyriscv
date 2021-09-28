from enum import Enum

class AluFunVal(Enum):
    NOP = 0
    XOR = 1
    COPY = 2
    SLTU = 3
    AND = 4
    ADD = 5
    SLT = 6
    SRA = 7
    SUB = 8
    SRL = 9
    SLL = 10
    OR = 11

class ALU:
    NUM_ALU_FUNS = 12

    ALU_FUN_SYMS = dict([
        (AluFunVal["NOP"], "X"),
        (AluFunVal["XOR"], "^"),
        (AluFunVal["COPY"], "cp"),
        (AluFunVal["SLTU"], "sltu"),
        (AluFunVal["AND"], "and"),
        (AluFunVal["ADD"], "add"),
        (AluFunVal["SLT"], "slt"),
        (AluFunVal["SRA"], "sra"),
        (AluFunVal["SUB"], "sub"),
        (AluFunVal["SRL"], "srl"),
        (AluFunVal["SLL"], "sll"),
        (AluFunVal["OR"], "or")
    ])

    print_on = False
    
    def alu(op1, op2, alu_fun):
        return getattr(ALU,
                       "_" + str(AluFunVal(alu_fun).name.lower())
                       )(op1, op2)
        
    def _nop(op1, op2):
        return 0     # abstract representation of no-op
                     # where the RISC-V CPU does something
                     # along the lines of addi x0, x0, 0

    def _xor(op1, op2):
        return op1 ^ op2

    def _copy(op1, op2):
        return op1

    def _sltu(op1, op2):
        if abs(op1) < abs(op2): return 1
        else: return 0

    def _and(op1, op2):
        return op1 & op2

    def _add(op1, op2):
        return op1 + op2

    def _slt(op1, op2):
        if op1 < op2: return 1
        else: return 0

    def _sra(op1, op2):
        return op1 >> op2

    def _sub(op1, op2):
        return op1 - op2

    def _srl(op1, op2):
        if op2 == 0: return op1
        return int(bin(op1)[:-op2], 2)

    def _sll(op1, op2):
        return op1 << op2

    def _or(op1, op2):
        return op1 | op2

if __name__ == "__main__":
    op1 = 0x100
    op2 = 0x2
    for alu_fun in range(ALU.NUM_ALU_FUNS):
        print(f"{op1:x} {ALU.ALU_FUN_SYMS[AluFunVal(alu_fun)].rjust(4, ' ')} {op2:x} = {ALU.alu(op1, op2, alu_fun):x}")
