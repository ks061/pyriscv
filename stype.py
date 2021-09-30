from pydigital.utils import sextend

class SType:
    _imm: int
    
    def set_imm(imm: int):
        SType._imm = imm

    get_imm = lambda: sextend(SType._imm, 12) 
        
