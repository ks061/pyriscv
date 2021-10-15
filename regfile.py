"""
Name: Kartikeya Sharma
Class: CSCI 320
Professor Marchiori

This file contains a static class
representing the register file within
the RISC-V Sodor 1-Stage processor.
"""

# Imports
import random
from riscv_isa.isa import regNumToName
from util import Util

"""
Static class representing the register
file within the RISC-V Sodor 1-Stage processor
"""
class RegFile:
	# number of registers
        # contained within the register
        # file
	NUM_REGS = 32

	# max num of bits to represent each one
        # of the registers
	REG_BIT_LEN = Util.calc_bit_len(NUM_REGS)

	# how many registers to print
        # on each line
	NUM_REGS_PER_LINE = 4
	# until how many chars to left-pad
        # register names with spaces
	NUM_STR_PADDING = 4

	# array of register values indexed
        # by register number
	reg_vals = [0 if i == 0 else None for i in range(NUM_REGS)]
	
	# private rs1 and rs2 fields
        # made accessible through the lambda
        # functions, which represent wires in 
        # hardware, get_rs1 and get_rs2, respectively
	_rs1 = None
	_rs2 = None
	get_rs1 = lambda: RegFile._rs1 
	get_rs2 = lambda: RegFile._rs2

	def read(rs1_index, rs2_index):
            if rs1_index != None:
                RegFile._rs1 = RegFile.reg_vals[rs1_index] 
            if rs2_index != None:
                RegFile._rs2 = RegFile.reg_vals[rs2_index]

	def clock(wa, wd, en):    
            if wa == None:
                return
            if wd == -1 or wd == None:
                return
            if en == True:
                RegFile.reg_vals[wa] = wd
	
	def display():
                out_str = ""
                reg_num = 0
                while (reg_num < RegFile.NUM_REGS):
                        for i in range(RegFile.NUM_REGS_PER_LINE):
                                out_str += str(regNumToName(reg_num))\
                                           .rjust(RegFile.NUM_STR_PADDING) +\
                                           ": "
                                if RegFile.reg_vals[reg_num] == None:
                                    out_str += "xxxxxxxx"
                                else:
                                    out_str += \
                                        f"{RegFile.reg_vals[reg_num]:08x}"
                                reg_num += 1
                        out_str += "\n"
                print(out_str)	
		
if __name__ == "__main__":

	# TESTING WRITING TO REGISTER FILE
        # THROUGH ITS CLOCK METHOD

	# Writing 0x42 plus the identification number
        # to each correspond register into the register
	# file
	RegFile.display()
	for wa in range(RegFile.NUM_REGS):
		RegFile.clock(wa, 0x42+wa, True) 
	RegFile.display()


	# TESTING READING FROM REGISTER FILE
	# THROUGH ITS READ METHOD
	
	# Picks random two registers to read from
	# and then reads the values of those two
        # registers from wires for rs1 and rs2
	for i in range(3):
		rs1 = random.randint(0, RegFile.NUM_REGS-1)
		rs2 = random.randint(0, RegFile.NUM_REGS-1)
		RegFile.read(rs1, rs2)
		
		# an index of 0 = zero, 1 = ra, that is, when
                # we compare the indices here to the ones given
                # in the testbench table of registers above
		print("rs1 index is " + str(rs1)) 
		# the value of the corresponding register
		print("rs1 value is 0x" + f"{RegFile.get_rs1():x}")
		print("rs2 index is " + str(rs2))
		print("rs2 value is 0x" + f"{RegFile.get_rs2():x}")		 

		print()
