"""
Modified fetch_decode.py in the 
pyriscv folder within the RISC-V
Sodor 1-Stage processor lab series

Kartikeya Sharma
Class: CSCI 320
Professor Marchiori
"""

# filename: fetch_decode.py
from alu import ALU, AluFunVal
from branch_cond_gen import BranchCondGen
from branch_targ_gen import BranchTargGen
from control_signals import ControlSignals
from datamem import DataMem
from pydigital.elfloader import load_elf
import itertools
from itype import IType
from jump_targ_gen import JumpTargGen
from jump_reg_targ_gen import JumpRegTargGen
from mux import make_mux
import os 
from pydigital.memory import readmemh, Memory, MemorySegment
from pydigital.register import Register
from pydigital.utils import sextend, as_twos_comp
from regfile import RegFile
from riscv_isa.csrs import CsrMemory
from riscv_isa.isa import Instruction, regNumToName
from riscv_isa.instr_codes import instrTypes
from stype import SType
import sys
from utype import UType

ALL_PRINT_ON = False
ALL_PRINT_OFF = False
if ALL_PRINT_ON:
   PRINT_DEBUG_ON = True
   PRINT_ECALL_ON = True
   PRINT_FINAL_REG_ON = True
   PRINT_FUNC_ON = True
   PRINT_INSTR_ON = True
   PRINT_LINUX_SYSCALL_ON = True
   PRINT_REG_ON = True
   PRINT_SYSCALL_ON = True
elif ALL_PRINT_OFF:
   PRINT_DEBUG_ON = False
   PRINT_ECALL_ON = False
   PRINT_FINAL_REG_ON = False
   PRINT_FUNC_ON = False
   PRINT_INSTR_ON = False
   PRINT_LINUX_SYSCALL_ON = False
   PRINT_REG_ON = False
   PRINT_SYSCALL_ON = False
else:
   # customize
   PRINT_DEBUG_ON = False
   PRINT_ECALL_ON = False
   PRINT_FINAL_REG_ON = False
   PRINT_FUNC_ON = False
   PRINT_INSTR_ON = False
   PRINT_LINUX_SYSCALL_ON = True
   PRINT_REG_ON = False
   PRINT_SYSCALL_ON = False

# the PC register
PC = Register()

def display():
   if instr == None:
       return "PC: xxxxxxxx, IR: xxxxxxxx"
   else:
       return f"PC: {PC.out():08x}, IR: {instr.val:08x}, {instr}"

def _get_debug_str():
   # retrieval of params for debugging
   rs1_index = instr.get_rs1() 
   rs2_index = instr.get_rs2()
   rd_index = instr.get_rd()
   if rs1_index != None: rs1_val = RegFile.get_rs1()
   else: rs1_val = None
   if rs2_index != None: rs2_val = RegFile.get_rs2()
   else: rs2_val = None
   if rd_index != None: rd_val = RegFile.reg_vals[instr.get_rd()]
   else: rd_val = None
   i_imm = instr.get_imm() 
   op = instr.get_opcode()
   func3 = instr.get_funct3()
   func7 = instr.get_funct7()
   alu_fun_index = ControlSignals.get_alufun()
   alu_fun = AluFunVal(alu_fun_index).name
   
   UNKNOWN_REG_VAL = "xxxxxxxx"
   UNKNOWN_REG_INDEX = " [xXX]"
   if i_imm == None: i_imm = 0
   if func3 == None: func3 = 0
   if func7 == None: func7 = 0

   debug_str = " rd: "
   if rd_val == None or rd_index == None: debug_str += UNKNOWN_REG_VAL
   else: debug_str += f"{rd_val:8x}"
   if rd_index == None: debug_str += UNKNOWN_REG_INDEX
   else: debug_str += f" [x{rd_index:2d}]"
   debug_str += " rs1: "
   if rs1_val == None or rs1_index == None: debug_str += UNKNOWN_REG_VAL
   else: debug_str += f"{rs1_val:8x}"
   if rs1_index == None: debug_str += UNKNOWN_REG_INDEX
   else: debug_str += f" [x{rs1_index:2d}]"
   debug_str += " rs2: "
   if rs2_val == None or rs2_index == None: debug_str += UNKNOWN_REG_VAL
   else: debug_str += f"{rs2_val:8x}"
   if rs2_index == None: debug_str += UNKNOWN_REG_INDEX
   else: debug_str += f" [x{rs2_index:2d}]"
   debug_str += " imm: "
   debug_str += f"{i_imm:04x}"
   debug_str += f" op: {op:02x}"
   debug_str += " func3: "
   debug_str += f"{func3}"
   debug_str += " func7: "
   debug_str += f"{func7}"
   debug_str += f" alu_fun: ALU_{alu_fun}"
   return debug_str

def full_display():
   if PRINT_INSTR_ON:
       # print one line w/ instruction
       print(f"{t:20d}:", display())

   if PRINT_DEBUG_ON:
       # then display debug line
       print(_get_debug_str())
       print()
       
   if PRINT_REG_ON:
       # then display regs
       RegFile.display()

def _handle_ecall():
   if instr._mnemonic.upper() == "ECALL":
       if RegFile.reg_vals[10] == 0:
           if PRINT_ECALL_ON: print("ECALL(0): HALT")
           return True # if returns True, processor must stop
       if RegFile.reg_vals[10] == 1:
           if PRINT_ECALL_ON: print("ECALL(" + str(RegFile.reg_vals[10]) +\
                                    "): " + str(RegFile.reg_vals[11]))
       if RegFile.reg_vals[10] == 10:
           if PRINT_ECALL_ON:print("ECALL(10): EXIT")
           return True
   return False

# mux setup helper funcs
def _raise_jalr_pc_sel_excep():
    raise Exception("jalr pc selection not implemented.")

def _raise_excep_pc_sel_excep():
    raise Exception("exception pc selection not implemented.")

# mux setup
pc_sel_mux = make_mux(
    lambda: PC.out() + 4,
    JumpRegTargGen.get_jalr,
    BranchTargGen.get_branch,
    JumpTargGen.get_jump,
    lambda: _raise_excep_pc_sel_excep()
)

op1sel_mux = make_mux(RegFile.get_rs1, UType.get_imm)
op2sel_mux = make_mux(RegFile.get_rs2, SType.get_imm, IType.get_imm, lambda : sextend(pc_val))

WORD_SIZE_BITS = 32
WORD_SIZE_BYTES = int(WORD_SIZE_BITS / 8) # 2 binary places right shift to
                    # go from byte address to  word address
wb_sel_mux = make_mux(DataMem.get_read_data, # non-implemented input;
                                  # mux index reserved
                      lambda: alu_out,
                      lambda: sextend(pc_val+4),
                      lambda: -1) # not implemented; placeholder      

data_mem = None

sym_table = None
# handle syscall
def _handle_syscall():
    if ControlSignals.get_mem_rw() == 0: return False
    if "tohost" not in sym_table: return False
    # val = imem[sym_table["tohost"]]
    DataMem.read(sym_table["tohost"], byte_count = 4, signed=False)
    val_lower = DataMem.get_read_data()
    DataMem.read(sym_table["tohost"]+4, byte_count = 4, signed=False)
    val_upper = DataMem.get_read_data()
    val = (val_upper << 32) + val_lower
    # dest_addr = ALU.alu(op1sel_mux(ControlSignals.get_op1sel()),
    #                   op2sel_mux(ControlSignals.get_op2sel()), 
    #                   ControlSignals.get_alufun()
    #           )
    # stop computing ALU result, just do it ONCE and save the value.
    dest_addr = alu_out
    dest_addr = as_twos_comp(dest_addr)
    if dest_addr == sym_table["tohost"]+4:
       if (val & 0x1) == 0x1:
           if PRINT_SYSCALL_ON: print(f"SYSCALL: exit ({val>>1})")
           if PRINT_FINAL_REG_ON:
               print("Final register values")
               RegFile.display()
           sys.exit(val>>1)
       else:
          try:
              DataMem.read(val, byte_count = 8, signed = True)
              which = DataMem.get_read_data()
          except:
              return
          if which != 64: return
          DataMem.read(val+8, byte_count = 8, signed = True)
          arg0 = DataMem.get_read_data()
          DataMem.read(val+16, byte_count = 8, signed = True)
          arg1 = DataMem.get_read_data()
          DataMem.read(val+24, byte_count = 8, signed = True)
          arg2 = DataMem.get_read_data()
          if PRINT_SYSCALL_ON: print(DataMem._mem.mem[arg1:arg1+arg2].decode("ASCII"), end="")
          DataMem._mem.mem[sym_table['fromhost']] = 1

def _handle_linux_syscall():
   if RegFile.reg_vals[17] != 93: return False
   ret_code = RegFile.reg_vals[10]
   if ret_code == None: return False
   if ret_code & 0x1 != 0:
       if PRINT_LINUX_SYSCALL_ON: print(f"TEST #0x{ret_code>>1:x} FAIL")
       sys.exit()
 
def _print_func_header(addr, reset=False):
    # if reset: name = "reset"
    # else: 
    #     name = "func not found" # if not found at end of this for loop
    #     for key, value in sym_table.items():
    #         if value == addr: name = key
    
    if PRINT_FUNC_ON and addr in sym_table: print(f"------------------------------<       {sym_table[addr]}        >------------------------------")

csr_mem = CsrMemory()

def _handle_csr():
    csr = (instr.val & 0xfff00000) >> 20
    mnemonic = instr.get_mnemonic()
    # print(mnemonic)
    rs1 = (instr.val & 0x000f8000) >> 15
    value = RegFile.reg_vals[rs1]
    cycle = t
    init_csr_val = csr_mem.clock(csr, mnemonic, value, cycle) 
    
    instr._rd = (instr.val & 0x00000f80) >> 7
    
    csr_rf_wen = 1 
    RegFile.clock(
        wa=instr.get_rd(), 
        wd=init_csr_val,
        en=csr_rf_wen
    )

data_paths = []
if len(sys.argv) < 2: data_paths.append('riscv_isa/programs/return')
else: 
    for i in range(len(sys.argv)-1):
        data_paths.append(sys.argv[i+1])

# init other vars for processor loop
global startup
global instr
global t
global maXkcycles
startup = None
instr = None
t = None
maXkcycles = 0

i = -1
while i < len(data_paths)-1:
   i = i+1
   #print('DATA PATH IS', data_paths, i, len(data_paths))
   data_path = data_paths[i]
   
   if data_path[0] == "-":
       if data_path[1] == "x":
           i = i+1
           maXkcycles = int(data_paths[i])
       continue

   elf_load_data = load_elf(data_path, quiet = not PRINT_DEBUG_ON)
   elf_imem = elf_load_data[0]
   sym_table = elf_load_data[1]
   imem = elf_imem
   if not PRINT_DEBUG_ON:
       print(f"Running {data_path}")

   '''
   _mem_seg = MemorySegment(
      begin_addr = 0xE0000,
      count = (0xEFFFF - 0xE0000 + 1) >> 2,
      word_size = WORD_SIZE_BYTES
   )
   '''

   data_mem = DataMem.init(Memory(elf_imem))
   startup = True
   # generate system clocks until we reach a stopping condition
   # this is basically the run function from the last lab
   for t in itertools.count():
      # if t % 10000 == 0: print("cycle #: " + str(t))
      if maXkcycles != 0 and t >= maXkcycles:
          break
      # RESET the PC register
      if startup:
          if PRINT_INSTR_ON: print(f"{t:20d}:", display())
          startup=False 
          PC.reset(sym_table["_start"] - 4)
          _print_func_header(addr=None, reset=True)
          continue
      else:
          # select PC
          if PC.out() == None:
              PC.reset(sym_table["_start"])
              continue 
          else:
              PC.clock(as_twos_comp(pc_sel_mux(ControlSignals.get_pc_sel())))

          pc_val = PC.out()

          if imem[pc_val] == 0:
              print("Done -- end of program.")
              break
    #   if t > 37: break
      # access instruction memory
      #if instr != None:
          #if instr.get_mnemonic().upper() == "JAL":          
              #_print_func_header(PC.out()) 
      if imem[pc_val] == 0x30200073: # mret = nop; not implemented in standard RISC-V ISA
         if PRINT_INSTR_ON:
            print(f"{t:20d}: mret instruction; ")
            print("nop b/c not implemented in standard RISC-V ISA") 
         ControlSignals.set_pc_sel(0)
         continue
      instr = Instruction(imem[pc_val], pc_val)

      _print_func_header(pc_val)
      if instr.is_csr():
         if PRINT_INSTR_ON: print(f"{t:20d}:", display())
         ControlSignals.set_pc_sel(0)
         _handle_csr()
         continue
      if instr._get_instr_name_equivalence(["FENCE"]):
         if PRINT_INSTR_ON: print(f"{t:20d}:", display())
         ControlSignals.set_pc_sel(0)
         continue
      # set control signals
      ControlSignals.set_instr_name(instr.get_mnemonic().lower())

      # process imm combinational blocks
      BranchTargGen.set_branch(
          PC.out(),
          (instr.get_val() >> 7) & 0x1f,
          (instr.get_val() >> 25) & 0x7f
      )
      JumpTargGen.set_jump(
          PC.out(),
          (instr.get_val() >> 12) & 0xfffff
      ) 
      IType.set_imm(instr.get_val() >> 20)
      SType.set_imm(
      ((instr.get_val() >> 25) << 5) +
      ((instr.get_val() >> 7) & 0x1f)
      )
      #UType.set_imm(instr.get_val() >> 12)
      UType.set_imm(sextend(instr.get_val() & 0xfffff000))

      # update instr imm from imm combo block
      # handling imm's for current instr type   
      instr.update_imm()
      # if instr._type == instrTypes.U: print(f"{instr._imm:x}")

      # regfile reading (combinational block)
      rs1_index = instr.get_rs1() 
      rs2_index = instr.get_rs2()
      rd_index = instr.get_rd()
      RegFile.read(rs1_index, rs2_index)

      BranchCondGen.set_branch_conds(
          RegFile.get_rs1(),
          RegFile.get_rs2()
      )

      # if previous instuction was a branch 
      # instruction, then see if branch was taken
    #   print(f"==={instr._mnemonic}={BranchCondGen.get_br_lt()}===")

      
      if ((instr._get_instr_name_equivalence(["BEQ"]) and
         BranchCondGen.get_br_eq()) or
         (instr._get_instr_name_equivalence(["BNE"]) and
         (not BranchCondGen.get_br_eq())) or
         (instr._get_instr_name_equivalence(["BLT"]) and
         BranchCondGen.get_br_lt()) or
         (instr._get_instr_name_equivalence(["BGE"]) and
         (not BranchCondGen.get_br_lt())) or
         (instr._get_instr_name_equivalence(["BLTU"]) and
         BranchCondGen.get_br_ltu()) or
         (instr._get_instr_name_equivalence(["BGEU"]) and
         (not BranchCondGen.get_br_ltu()))):  
          ControlSignals.set_pc_sel(2)
          full_display()
          continue
      elif instr._type == instrTypes.UJ:
          ControlSignals.set_pc_sel(3)
      elif instr._get_instr_name_equivalence(["JALR"]):
          ControlSignals.set_pc_sel(1)
      else:
          ControlSignals.set_pc_sel(0)


      # after IType calculated
      JumpRegTargGen.set_jalr(RegFile.get_rs1(), IType.get_imm())
      
      # select op1 and op2
      op1=op1sel_mux(ControlSignals.get_op1sel())
      op2=op2sel_mux(ControlSignals.get_op2sel())

      # compute alu output
      alu_out = ALU.alu(op1,op2,ControlSignals.get_alufun())

      if instr._get_instr_name_equivalence(["LBU", "LHU", "LWU"]):
         signed = False
      else:
         signed = True
      DataMem.exec(
          addr = alu_out,
          wdata = RegFile.get_rs2(), 
          mem_rw = ControlSignals.get_mem_rw(),
          mem_val = ControlSignals.get_mem_val(),
          signed = signed
      )
      wb_val = wb_sel_mux(ControlSignals.get_wb_sel())
      #print(f"wb_val is {wb_val: 08x}")
      # regfile writing
      RegFile.clock(
          wa=instr.get_rd(), 
          wd=wb_val,
          en=ControlSignals.get_rf_wen()
      )

      full_display()

      # then handle ECALL
      if _handle_ecall(): break # if instr was ecall and dictates processor
                                # stopping, i.e. halt or exit, break out of loop

      # then handle SYSCALL   
      if _handle_syscall(): break # break for exit if specified by syscall

      # then handle Linux SYSCALL
      if instr.get_mnemonic() == 'ecall' and _handle_linux_syscall(): break

   if PRINT_FINAL_REG_ON:
      print("Final register values")
      RegFile.display()
   
   if PRINT_LINUX_SYSCALL_ON: print("TEST PASS")
