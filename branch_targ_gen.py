from pydigital.utils import sextend

class BranchTargGen:
    _branch: int

    def set_branch(pc: int, ir_7_11: int, ir_25_31: int):
        imm_0 = 0
        imm_11 = ir_7_11 & 0x1
        imm_1_4 = ir_7_11 >> 1
        imm_5_10 = ir_25_31 & 0x3f
        imm_12 = ir_25_31 >> 6
        imm = \
            imm_0 + (imm_1_4 << 1) +\
            (imm_5_10 << 5) + (imm_11 << 11) +\
            (imm_12 << 12)
        BranchTargGen._branch = pc + sextend(imm, 13)

    get_branch = lambda: BranchTargGen._branch 
