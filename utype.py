from pydigital.utils import sextend, as_twos_comp

class UType:
    _imm: int
    
    def set_imm(imm: int):
        UType._imm = imm
        # print(f"0x{UType._imm:x}")
        # print(as_twos_comp(UType._imm))
        # print(sextend(as_twos_comp(UType._imm), 20) << 12)
    get_imm = lambda: sextend(as_twos_comp(UType._imm), 20) << 12
        
