from enum import Enum

class instrOpcode(Enum):
	LB = LH = LW = LD = LBU = LHU = LWU = 0x03
	FENCE = FENCE_I = 0x0f
	ADDI = SLLI = SLTI = SLTIU = XORI = SRLI = SRAI = ORI = ANDI = 0x13
	AUIPC = 0x17
	ADDIW = SLLIW = SRLIW = SRAIW = 0x1b
	SB = SH = SW = SD = 0x23
	ADD = SUB = SLL = SLT = SLTU = XOR = SRL = SRA = OR = AND = 0x33
	LUI = 0X37
	ADDW = SUBW = SLLW = SRLW = SRAW = 0x3b
	BEQ = BNE = BLT = BGE = BLTU = BGEU = 0x63
	JALR = 0X67
	JAL = 0x6f
	ECALL = EBREAK = CSRRW = CSRRS = CSRRC = CSRRWI = CSRRSI = CSRRCI = \
		0x73

		# LI = 0x13
		# ADD = 0x33
		# ECALL = 0x73 

class instrFunct3(Enum):
	LB = FENCE = ADDI = ADDIW = SB = ADD = SUB = ADDW = SUBW = BEQ = \
	JALR = ECALL = BREAK = 0x0

	LH = FENCE_I = SLLI = SLLIW = SH = SLL = SLLW = BNE = CSRRW = 0x1
	LW = SLTI = SW = SLT = CSRRS = 0x2
	LD = SLTIU = SD = SLTU = CSRRC = 0x3
	LBU = XORI = XOR = BLT = 0x4

	LHU = SRLI = SRLA = SRLIW = SRAIW = SRL = SRA = SRLW = SRAW = \
	BGE = CSRRWI = 0x5
		
	LWU = ORI = OR = BLTU = CSRRSI = 0x6
	ANDI = AND = BGEU = CSRRCI = 0x7

class instrFunct7(Enum):
	SLLI = SRLI = SLLIW = SRLIW = ADD = SLL = SLT = SLTU = XOR = \
	SRL = OR = AND = ADDW = SLLW = SRLW = ECALL = 0x00
		
	EBREAK = 0x001

	SRAI = SRAIW = SUB = SRA = SUBW = SRAW = 0x20

class instrTypes(Enum):
	R = 0
	I = 1
	S = 2
	SB = 3
	U = 4
	UJ = 5
