from pydigital.utils import sextend, as_twos_comp

class JumpTargGen:
    _jump: int

    def set_jump(pc: int, ir_12_31: int):
        imm_0 = 0
        imm_12_19 = ir_12_31 & 0xff
        imm_11 = (ir_12_31 >> 8) & 0x1
        imm_1_10 = (ir_12_31 >> 9) & 0x3ff
        imm_20 = (ir_12_31 >> 19) & 0x1 
        imm = \
            imm_0 + (imm_1_10 << 1) +\
            (imm_11 << 11) + (imm_12_19 << 12) +\
            (imm_20 << 20)
        JumpTargGen._jump = as_twos_comp(pc + sextend(imm, 20)) & 0xffffffff

    get_jump = lambda: JumpTargGen._jump
        
