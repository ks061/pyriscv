"""
Name: Kartikeya Sharma
Class: CSCI 320
Professor Marchiori

This file contains a static class
representing the data memory unit within
the RISC-V Sodor 1-Stage processor.
"""

# Imports
from pydigital.memory import MemorySegment, Memory
from pydigital.utils import as_twos_comp, sextend

"""
Static class representing the data memory
unit within the RISC-V Sodor 1-Stage processor
"""
class DataMem:
    _mem = None

    _read_data = None
    get_read_data = lambda: DataMem._read_data

    # initializing the class, 
    # not an instance
    def init(mem):
        DataMem._mem = mem

    def exec(addr, wdata, mem_rw, mem_val = 4, signed = True):
        addr = as_twos_comp(addr)
        if mem_val not in [1, 2, 4, 8]: return        
        if mem_rw == 0: DataMem.read(addr,
                                     byte_count=mem_val,
                                     signed=signed)
        else: DataMem.clock(addr,
                            wdata,
                            mem_rw,
                            byte_count=mem_val)

    def read(addr, byte_count, signed):
        try: 
             DataMem._read_data = DataMem._mem.out(addr,
                                                   byte_count=byte_count,
                                                   signed=signed)
        except IndexError: # memory segment not found
                           # probably b/c invalid addr
                           # in turn b/c wasn't an lw 
                           # or sw instr
            return

    def clock(addr,
              wdata,
              mem_rw,
              byte_count):
        wdata = as_twos_comp(wdata)
        DataMem._mem.clock(addr, wdata, mem_rw, byte_count=byte_count)

if __name__ == "__main__":
    pass
