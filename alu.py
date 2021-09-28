"""
Name: Kartikeya Sharma
Class: CSCI 320
Professor Marchiori

This file contains a static class
representing the ALU in the RISC-V
Sodor 1-Stage processor. It contains
the functions nop, xor, copy, sltu,
and, add, slt, sra, sub, srl, sll, or.
"""

from enum import Enum

"""
Represents ALU function values
for each operation
"""
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

"""
Static class representing the ALU
in the RISC-V Sodor 1-Stage processor,
containing the operations nop, xor,
copy, sltu, and, add, slt, sra, sub,
srl, sll, or.
"""
class ALU:
    # number of operations
    # that this ALU can perform
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
        if op1 < 0: return -((-op1) >> op2)
        else: return op1 >> op2
	
    def _sll(op1, op2):
        return op1 << op2

    def _or(op1, op2):
        return op1 | op2

if __name__ == "__main__":
    # Test is modeled after the
    # test given in the
    # lab assignment
    
    print("Test 1 (Note: output values " +\
          "are given in hex)")
    
    op1 = 0x100
    op2 = 0x2
    
    for alu_fun in range(ALU.NUM_ALU_FUNS):
        print(f"{op1:x} " + \
	      f"{ALU.ALU_FUN_SYMS[AluFunVal(alu_fun)].rjust(4, ' ')}" + \
	      f" {op2:x} " + \
	      f"= {ALU.alu(op1, op2, alu_fun):x}"
	)

    print()

    # The remainder of the
    # are fairly straight forward
    # and, consequently, do not
    # really require testing (almost).
    # There is one exception: the tricky
    # srl (shift right logical) in Python
    
    # I will test this with a combination
    # of positive and negative numbers.

    print("Test 2: testing srl")

    alu_fun = 9

    op1 = -1
    op2 = 1
    
    print("-1 srl 1")
    print("Expected: 0")
    print("Actual: " + str(ALU.alu(op1, op2, alu_fun)))
    
    print()

    op1 = -64
    op2 = 3

    print("-64 srl 3")
    print("Expected: -8")
    print("Actual: " + str(ALU.alu(op1, op2, alu_fun)))
