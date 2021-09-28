import random
from riscv_isa.isa import regNumToName
from util import Util

class RegFile:

	NUM_REGS = 32

	REG_BIT_LEN = Util.calc_bit_len(NUM_REGS)

	NUM_REGS_PER_LINE = 4
	NUM_STR_PADDING = 4

	reg_vals = [0 for i in range(NUM_REGS)]
	_rs1 = None
	_rs2 = None

	get_rs1 = lambda: RegFile._rs1 
	get_rs2 = lambda: RegFile._rs2

	def read(rs1_index, rs2_index):
		RegFile._rs1 = RegFile.reg_vals[rs1_index] 
		RegFile._rs2 = RegFile.reg_vals[rs2_index]

		return

	def clock(wa, wd, en):
		if en is True and wa != 0:
			RegFile.reg_vals[wa] = wd
		return

	def display():
		out_str = ""
		reg_num = 0
		while (reg_num < RegFile.NUM_REGS):
			for i in range(RegFile.NUM_REGS_PER_LINE):
				out_str += \
				str(regNumToName(reg_num))\
				.rjust(RegFile.NUM_STR_PADDING) +\
				 ": " + f"{RegFile.reg_vals[reg_num]:08x}" + " "
				reg_num += 1
			out_str += "\n"
		print(out_str)	
		
if __name__ == "__main__":
	RegFile.display()
	for wa in range(RegFile.NUM_REGS):
		RegFile.clock(wa, 0x42+wa, True) 
	RegFile.display()

	for i in range(3):
		rs1 = random.randint(0, RegFile.NUM_REGS-1)
		rs2 = random.randint(0, RegFile.NUM_REGS-1)
		print("rs1 index is " + str(rs1))
		print("rs2 index is " + str(rs2))

		RegFile.read(rs1, rs2)
	
		print("rs2 value is 0x" + f"{RegFile.get_rs2():x}")		 
		print("rs1 value is 0x" + f"{RegFile.get_rs1():x}")
