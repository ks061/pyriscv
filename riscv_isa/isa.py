from .csr_list import csrs
from enum import Enum

class BadInstruction(Exception):
    pass

# build csr lookup
csrd = {k:v for k,v in csrs}

def regNumToName(num):
    if type(num) != int or num < 0 or num > 31:
        raise BadInstruction()
    return ['zero','ra','sp','gp',  # 0..3
            'tp', 't0', 't1', 't2', # 4..7
            's0', 's1', 'a0', 'a1', # 8..11
            'a2', 'a3', 'a4', 'a5', # 12..15
            'a6', 'a7', 's2', 's3', # 16..19
            's4', 's5', 's6', 's7', # 20..23
            's8', 's9', 's10', 's11', # 24..27]
            't3', 't4', 't5', 't6'][num] # 28..31

class instrMnemonic(Enum):
    LI = 0x13
    ADD = 0x33
    ECALL = 0x73 

class instrTypes(Enum):
    R = 0
    I = 1
    S = 2
    SB = 3
    U = 4
    UJ = 5

class Instruction():
    "represents/decodes RISCV instructions"  

    def __init__ (self, val, pc, symbols = {}):
        """
        Decodes a risc-v instruction word
        val is the machine code word
        pc is the pc value used to format pc-relative assembly instructions
        symbols is an optional symbol table to decode addresses in assembly output 
        """
        self.val = val        
        self.pc = pc # pc relative instrs need pc to compute targets for display
        self.symbols = symbols

        self._opcode = None
        self._rsd = None
        self._funct3 = None
        self._rs1 = None
        self._rs2 = None
        self._funct7 = None
        self._imm = None
            
        self._mnemonic = None
        self._type = None


    def _reset_instr_components(self):
        self._opcode = None
        self._rsd = None
        self._funct3 = None
        self._rs1 = None
        self._rs2 = None
        self._funct7 = None
        self._imm = None

        self._mnemonic = None 
        self._type = None
        
    def _decode_and_set_mnemonic(self):
        if self._opcode == instrMnemonic.LI.value:
                self._mnemonic = instrMnemonic.LI
        if self._opcode == instrMnemonic.ADD.value:
                self._mnemonic = instrMnemonic.ADD
        if self._opcode == instrMnemonic.ECALL.value:
                self._mnemonic = instrMnemonic.ECALL

    def _decode_and_set_type(self):
        if self._mnemonic == instrMnemonic.LI:
                self._type = instrTypes.I
        if self._mnemonic == instrMnemonic.ADD:
                self._type = instrTypes.R
        if self._mnemonic == instrMnemonic.ECALL:
                self._type = instrTypes.I

    def _decode_and_set_by_type(self, temp_val: int):
        if self._type == instrTypes.I: self._decode_i_instr(temp_val)
        if self._type == instrTypes.R: self._decode_r_instr(temp_val)

    def _decode_i_instr(self, temp_val: int):
        self._rd = temp_val & 0x1f
        temp_val = temp_val >> 5
        self._funct3 = temp_val & 0x7
        temp_val = temp_val >> 3
        self._rs1 = temp_val & 0x1f
        temp_val = temp_val >> 5
        self._imm = temp_val

    def _decode_r_instr(self, temp_val: int):
        self._rd = temp_val & 0x1f
        temp_val = temp_val >> 5
        self._funct3 = temp_val & 0x7
        temp_val = temp_val >> 3
        self._rs1 = temp_val & 0x1f
        temp_val = temp_val >> 5
        self._rs2 = temp_val & 0x1f
        temp_val = temp_val >> 5
        self._funct7 = temp_val

    def decode_and_set_instr_components(self):
        self._mnemonic = None

        temp_val = self.val # make temp variable for extracting
                            # bits from instruction hex value

        self._opcode = temp_val & 0x7f # set lower 7 bits
                                       # to opcode instruction attribute

        temp_val = temp_val >> 7 # push off 7 extracted LSBs
        
        self._decode_and_set_mnemonic()
        self._decode_and_set_type()
        self._decode_and_set_by_type(temp_val)
        
    def __str__ (self):
        self.decode_and_set_instr_components()

        str_out = self._mnemonic.name.lower() + " "
        if self._mnemonic == instrMnemonic.LI:
                return str_out + regNumToName(self._rd) + "," +\
                       str(self._imm)
        elif self._mnemonic == instrMnemonic.ECALL:
                return str_out
        elif self._mnemonic == instrMnemonic.ADD:
                return str_out + regNumToName(self._rd) + "," +\
                       regNumToName(self._rs1) + "," +\
                       regNumToName(self._rs2)
        else:
                return Exception("Cannot decode instructions other than " +\
                                 "R or I type at this time.")

		
 
