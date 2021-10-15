from pydigital.utils import sextend

class UType:
    _imm: int
    
    def set_imm(imm: int):
        UType._imm = imm

    get_imm = lambda: sextend(UType._imm, 20) << 12
        
