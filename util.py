class Util:
	
	def calc_bit_len(reg_num):
		if reg_num == 1: return 0
		else: return 1 + Util.calc_bit_len(reg_num >> 1)	

