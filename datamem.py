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

    def exec(addr, wdata, mem_rw, mem_val = 4):
        if mem_val != 4: raise Exception("DataMem only built for 4-byte words")
        
        if mem_rw == 0: DataMem.read(addr)
        else: DataMem.clock(addr, wdata)

    def read(addr):
        try: 
             DataMem._read_data = DataMem._mem.out(addr)
        except IndexError: # memory segment not found
                           # probably b/c invalid addr
                           # in turn b/c wasn't an lw 
                           # or sw instr
            return

    def clock(addr, wdata):
        DataMem._mem.clock(addr, wdata, mem_rw=1)

if __name__ == "__main__":
    pass
