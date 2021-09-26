from riscv_isa.isa import regNumToName

class RegFile:

	NUM_REGS = 32
	NUM_REGS_PER_LINE = 4
	NUM_STR_PADDING = 4

	def __init__(self):
		self.reg_vals = [0 for i in range(32)]

	def read(rs):
		return

	def clock(wa, wd, en):
		return

	def display(self):
		print(self)
	
	def __str__(self):
		out_str = ""
		reg_num = 0
		while (reg_num < self.NUM_REGS):
			for i in range(self.NUM_REGS_PER_LINE):
				out_str += str(regNumToName(reg_num)).rjust(self.NUM_STR_PADDING) +\
				 ": " + f"{self.reg_vals[reg_num]:08x}" + " "
				reg_num += 1
			out_str += "\n"
		return out_str	
		
if __name__ == "__main__":
	rf = RegFile()
	rf.display()
	
