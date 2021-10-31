from pydigital.utils import sextend, as_twos_comp

class UType:
    _imm: int
    
    def set_imm(imm: int):
        UType._imm = imm
    
    get_imm = lambda: sextend(UType._imm, c=20) << 12
        
