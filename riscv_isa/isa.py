from .csr_list import csrs
from .instr_codes import instrOpcode, instrFunct3, instrFunct7, instrTypes

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

                self._reset_instr_components()

                self.decode_and_set_instr_components()
        
        def decode_and_set_instr_components(self):
                self._decode_and_set_mnemonic()
                self._decode_and_set_type()
                self._decode_by_type_and_set_bits()

        def _get_candidates_with_funct_3(self, instr_candidate_names):
                candidates_with_funct3 = []
                for funct3_item_name, funct3_item in instrFunct3.__members__.items():
                        for candidate_name in instr_candidate_names:
                                if funct3_item_name == candidate_name: 
                                        candidates_with_funct3.append(candidate_name)
                return candidates_with_funct3

        def _get_candidates_with_funct_7(self, instr_candidate_names):
                candidates_with_funct7 = []
                for funct7_item_name, funct7_item in instrFunct7.__members__.items():
                        for candidate_name in instr_candidate_names:
                                if funct7_item_name == candidate_name: 
                                        candidates_with_funct7.append(candidate_name)
                return candidates_with_funct7

        def _decode_and_set_mnemonic(self):
                self._decode_and_set_opcode()
                
                instr_candidate_names = [item_name for item_name, item in instrOpcode.__members__.items()]

                for opcode_item_name, opcode_item in instrOpcode.__members__.items():
                        if opcode_item.value != self._opcode_bits:
                                instr_candidate_names.remove(
                                        opcode_item_name
                                )

                candidates_with_funct3 = self._get_candidates_with_funct_3(instr_candidate_names)
                funct3_match_found = False

                if len(candidates_with_funct3) > 0:
                        self._decode_and_set_funct3()
                        for candidate_with_funct3 in candidates_with_funct3:
                                if instrFunct3[candidate_with_funct3].value != self._funct3:
                                        instr_candidate_names.remove(
                                                candidate_with_funct3
                                        )
                                else: funct3_match_found = True

                
                candidates_with_funct7 = self._get_candidates_with_funct_7(instr_candidate_names)
                funct7_match_found = False
                
                if len(candidates_with_funct7) > 0:
                        self._decode_and_set_funct7()
                        for candidate_with_funct7 in candidates_with_funct7:
                                if instrFunct7[candidate_with_funct7].value != self._funct7:
                                        instr_candidate_names.remove(
                                                candidate_with_funct7
                                        )
                                else: funct7_match_found = True
                
                if not funct7_match_found: self._reset_funct7()
                if not funct3_match_found: self._reset_funct3()
 
                if len(instr_candidate_names) > 0:
                        self._mnemonic = instr_candidate_names[0]
                else:
                        print("No matching instructions found.")

        def _get_instr_code_equivalence(self, instr_name):
                if self._mnemonic == instrOpcode[instr_name].name:
                        return True
                return False
        
        def _decode_and_set_type(self):
                if self._get_instr_code_equivalence("ADDI") or \
                   self._get_instr_code_equivalence("ECALL"):
                        self._type = instrTypes.I
                if self._get_instr_code_equivalence("ADD"):
                        self._type = instrTypes.R

        def _decode_by_type_and_set_bits(self):
                if self._type == instrTypes.I: 
                        self._decode_i_instr_and_set_bits()
                if self._type == instrTypes.R: 
                        self._decode_r_instr_and_set_bits()

        def _decode_and_set_opcode(self):
                self._opcode_bits = self.val & 0x7f # set lower 7 bits
                                                    # to opcode instruction attribute

        def _decode_and_set_rd(self):
                self._rd = (self.val >> 7) & 0x1f
        
        def _decode_and_set_funct3(self):
                self._funct3 = (self.val >> 12) & 0x7

        def _decode_and_set_rs1(self):
                self._rs1 = (self.val >> 15) & 0x1f

        def _decode_and_set_rs2(self):
                self._rs2 = (self.val >> 20) & 0x1f

        def _decode_and_set_funct7(self):
                self._funct7 = (self.val >> 25)

        def _decode_i_instr_and_set_bits(self):
                self._decode_and_set_rd()
                self._decode_and_set_funct3()
                self._decode_and_set_rs1()
                self._imm = self.val >> 20 # extract immediate constant

        def _decode_r_instr_and_set_bits(self):
                self._decode_and_set_rd()
                self._decode_and_set_funct3()
                self._decode_and_set_rs1()
                self._decode_and_set_rs2()
                self._decode_and_set_funct7()

        
        def __str__ (self):
                str_out = str(self._mnemonic).lower() + " "
                
                if self._get_instr_code_equivalence("ADDI") and self._rs1 == 0x0:
                                str_out = "li "
                                return str_out + regNumToName(self._rd) + "," +\
                                           str(self._imm)
                elif self._get_instr_code_equivalence("ECALL"):
                                return str_out
                elif self._get_instr_code_equivalence("ADD"):
                                return str_out + regNumToName(self._rd) + "," +\
                                           regNumToName(self._rs1) + "," +\
                                           regNumToName(self._rs2)
                else:
                                raise Exception("Cannot decode instructions other than " +\
                                                                 "R or I type at this time.")

        def _reset_instr_components(self):
                self._opcode_bits = None
                self._funct3_bits = None
                self._funct7_bits = None
                self._mneumonic = None
                
                self._rsd = None
                self._rs1 = None
                self._rs2 = None
                self._imm = None
                        
                self._type = None

        def _reset_funct3(self):
                self._funct3 = None
                self._funct3_enum = None

        def _reset_funct7(self):
                self._funct7 = None
                self._funct7_enum = None

                
 
