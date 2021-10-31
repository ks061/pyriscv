from pydigital.utils import sextend, as_twos_comp

class IType:
    _imm: int
    
    def set_imm(imm: int):
        IType._imm = imm

    get_imm = lambda: sextend(IType._imm, 12)
        
