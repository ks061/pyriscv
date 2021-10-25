from pydigital.utils import sextend

class JumpRegTargGen:
    _jalr: int

    def set_jalr(rs1_val: int, i_imm: int):
        if rs1_val == None: return
        JumpRegTargGen._jalr = rs1_val + i_imm
    get_jalr = lambda: JumpRegTargGen._jalr
        
