from pydigital.utils import sextend, as_twos_comp

class JumpRegTargGen:
    _jalr: int

    def set_jalr(rs1_val: int, i_imm: int):
        if rs1_val == None: return
        JumpRegTargGen._jalr = as_twos_comp(rs1_val + i_imm) & 0xffffffff
    get_jalr = lambda: JumpRegTargGen._jalr
        
