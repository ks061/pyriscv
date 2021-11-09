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
from pydigital.utils import sextend, as_twos_comp

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
    
    def _check_op1_undef(op1):
        if op1 == None: raise Exception("ALU Exception: op1 not defined.")

    def _check_op2_undef(op2):
        if op2 == None: raise Exception("ALU Exception: op2 not defined.")
    
    def _check_op1_op2_undef(op1, op2):
        if op1 == None and op2 == None:
            raise Exception("ALU Exception: op1 and op2 not defined.")
        if op1 == None: ALU._check_op1_undef(op1)
        if op2 == None: ALU._check_op2_undef(op2)
            
    def alu(op1, op2, alu_fun):
        output = getattr(ALU,
                       "_" + str(AluFunVal(alu_fun).name.lower())
                       )(op1, op2)
        return output

    def _nop(op1, op2):
        return 0     # abstract representation of no-op
                     # where the RISC-V CPU does something
                     # along the lines of addi x0, x0, 0

    def _xor(op1, op2):
        ALU._check_op1_op2_undef(op1, op2)
        return op1 ^ op2

    def _copy(op1, op2):
        ALU._check_op1_undef(op1)
        return op1

    def _sltu(op1, op2):
        ALU._check_op1_op2_undef(op1, op2)
        if as_twos_comp(op1) < as_twos_comp(op2): return 1
        else: return 0

    def _and(op1, op2):
        ALU._check_op1_op2_undef(op1, op2)
        return op1 & op2

    def _add(op1, op2):
        ALU._check_op1_op2_undef(op1, op2)
        #return op1 + op2
        return sextend(0xffffffff & (as_twos_comp(op1) + as_twos_comp(op2)))

    def _slt(op1, op2):
        ALU._check_op1_op2_undef(op1, op2)
        if op1 < op2: return 1
        else: return 0

    def _sra(op1, op2):
        ALU._check_op1_op2_undef(op1, op2)
        """
        print(f"op1: {op1:09x}")
        print(f"sextend(op1): {sextend(op1):09x}")
        print(f"sextend(op1) >> op2: {sextend(op1) >> op2:09x}")
        """
        return op1 >> (0x1f & op2)

    def _sub(op1, op2):
        ALU._check_op1_op2_undef(op1, op2)
        #return op1 - op2
        return sextend(0xffffffff & (as_twos_comp(op1) - as_twos_comp(op2)))

    def _srl(op1, op2):
        ALU._check_op1_op2_undef(op1, op2)
        if op2 == 0: return op1 # not changing underlying
			       # value (result from op1)
        if op1 >= 0: return op1 >> op2 # if op1 pos, same as sra
        if op1 < 0: return int(hex(-op1), 16) >> op2
			   # if op1 neg, calculate -op1 (pos int) 
			   # sra op2 so sign-extending neg num 
			   # is not done by sra (due to not being done
			   # definitionally by srl). then, finally, return
			   # the shifted pos op1 by op2 result back into
			   # b/c op1, if shifted by op2>0, should be 
			   # positive (0s assumed to "shift in" on left
			   # due to no sign-extending in srl)
			   # by sra 
        else: return op1 >> op2
	
    def _sll(op1, op2):
        ALU._check_op1_op2_undef(op1, op2)
        # print(f"Doing SLL 0x{op1: 08x} << {(0x1f & op2):d}")
        out = sextend(as_twos_comp(op1 << (0x1f & op2)) & 0xffffffff)
        # print(f"SLL RESULT {out: 08x}")
        return out

    def _or(op1, op2):
        ALU._check_op1_op2_undef(op1, op2)
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

    # testbench helper returns string
    # representing result of ALU executor
    def _print_srl_exec(op1, 
                        op2,
                        exp_val, 
                        alu_fun=9 # for srl
    ):
        print(str(op1) + " srl " + str(op2))
        print("Expected: " + str(exp_val))
        print("Actual: " + str(ALU.alu(op1, op2, alu_fun)))
        print()

    # short form of _print_srl_exec()
    _psrl = _print_srl_exec
   
    _psrl(-4, 0, -4)
    _psrl(-4, 1, 2)
    _psrl(-4, 2, 1)
    _psrl(-4, 3, 0)

    _psrl(4, 0, 4)
    _psrl(4, 1, 2)
    _psrl(4, 2, 1)
    _psrl(4, 3, 0)
