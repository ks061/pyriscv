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
from control_signals import ControlSignals
import itertools
from itype import IType
from mux import make_mux 
from pydigital.memory import readmemh
from pydigital.register import Register
from pydigital.utils import sextend
from regfile import RegFile
from riscv_isa.isa import Instruction, regNumToName
from stype import SType
import sys
from utype import UType

# the PC register
PC = Register()
 
# construct a memory segment for instruction memory
# load the contents from the 32-bit fetch_test hex file (big endian)
if len(sys.argv) >= 2: mem_address = sys.argv[1]
else: mem_address = "riscv_isa/programs/fetch_test.hex"
imem = readmemh(mem_address,
   word_size = 4, byteorder = 'big')
 
def display():
   if pc_val == None:
       return "PC: xxxxxxxx, IR: xxxxxxxx"
   else:
       return f"PC: {pc_val:08x}, IR: {instr.val:08x}, {instr}"
 
startup = True
# generate system clocks until we reach a stopping condition
# this is basically the run function from the last lab
for t in itertools.count():
   # sample inputs
   pc_val = PC.out()
 
   # RESET the PC register
   if startup:
       PC.reset(imem.begin_addr)       
       startup = False
       print(f"{t:20d}:", display())
       continue
  
   # access instruction memory
   instr = Instruction(imem[pc_val], pc_val)
   print(instr)

   ControlSignals.set_instr_name(instr.get_mnemonic().lower())

   IType.set_imm(instr.get_val() >> 20)
   SType.set_imm(
       ((instr.get_val() >> 25) << 5) +
       ((instr.get_val() >> 7) & 0x1f)
   )
   UType.set_imm(instr.get_val() >> 12)
   
   rs1_index = instr.get_rs1() 
   rs2_index = instr.get_rs2()
   rd_index = instr.get_rd()
   if rs1_index is None: rs1_index = 0
   if rs2_index is None: rs2_index = 0
   if rd_index is None: rd_index = 0
   RegFile.read(rs1_index, rs2_index)
   op1sel_mux = make_mux(RegFile.get_rs1, UType.get_imm)
   op2sel_mux = make_mux(RegFile.get_rs2, SType.get_imm, IType.get_imm, pc_val)
  
   
   op1=op1sel_mux(ControlSignals.get_op1sel())
   op2=op2sel_mux(ControlSignals.get_op2sel())
   wb_sel_mux = make_mux(lambda: -1, # non-implemented input;
                                     # mux index reserved
                         lambda: ALU.alu(op1sel_mux(ControlSignals.get_op1sel()),
                                 op2sel_mux(ControlSignals.get_op2sel()), 
                                 ControlSignals.get_alufun()),
                         lambda: pc_val+4,
                         lambda: -1) # not implemented; placeholder      

   """
   print(f"wa = {instr.get_rd()}")
   print(f"wd = {wb_sel_mux(ControlSignals.get_wb_sel())}")
   print(f"en = {ControlSignals.get_rf_wen()}")   
   """

   RegFile.clock(
       wa=instr.get_rd(), 
       wd=wb_sel_mux(ControlSignals.get_wb_sel()),
       en=ControlSignals.get_rf_wen()
   )


   # print one line at the end of the clock cycle
   print(f"{t:20d}:", display())

   if instr._mnemonic.upper() == "ECALL":
       if RegFile.reg_vals[10] == 0:
           print("ECALL(0): HALT")
           exit()
       if RegFile.reg_vals[10] == 1:
           print("ECALL(" + str(RegFile.reg_vals[10]) + "): " + str(RegFile.reg_vals[11]))

   """
   rs1_val = RegFile.get_rs1()
   rs2_val = RegFile.get_rs2()
   rd_val = RegFile.reg_vals[instr.get_rd()]
   i_imm = instr.get_imm() 
   op = instr.get_opcode()
   func3 = instr.get_funct3()
   func7 = instr.get_funct7()
   alu_fun_index = ControlSignals.get_alufun()
   alu_fun = AluFunVal(alu_fun_index).name

   print(f"rd: {rd_val:8d} [x{rd_index:2d}] " +\
         f"rs1: {rs1_val:8d} [x{rs1_index:2d}] " +\
         f"rs2: {rs2_val:8d} [x{rs2_index:2d}] " +\
         f"i_imm: {i_imm:5d} " +\
         f"op: {op:04d} " +\
         f"func3: {func3} " +\
         f"func7: {func7} " +\
         f"alu_fun: ALU_{alu_fun}"
   )
   """

   # clock logic blocks, PC is the only clocked module!
   # here the next pc value is always +4
   PC.clock(4 + pc_val)
  
   # check stopping conditions on NEXT instruction
   if PC.out() > 0x1100:
       print("STOP -- PC is large! Is something wrong?")
       break
   if imem[PC.out()] == 0:
       print("Done -- end of program.")
       break

print("Final register values")
RegFile.display()
