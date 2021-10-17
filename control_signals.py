"""
Kartikeya Sharma
Course: CSCI 320
Professor Marchiori

This file contains the library
of control signals used
 in the RISC-V Sodor
1-Stage processor.
"""

import csv

class ControlSignals:

    _has_loaded_csv = False

    CSV_FILENAME_CTRL_SIGNALS = "data/decoder_ctrl_signals.csv"
    
    ROW_INDEX_HEADER = 1 
    ROW_INDEX_INSTR_BEGIN = 2
    ROW_INDEX_INSTR_END = 33
    
    COL_INDEX_INSTRUCTION = 0

    COL_INDEX_PC_SEL = 5
    COL_INDEX_ALUFUN = 6
    COL_INDEX_OP2SEL = 7
    COL_INDEX_OP1SEL = 8
    COL_INDEX_WB_SEL = 9
    COL_INDEX_RF_WEN = 10
    COL_INDEX_MEM_RW = 11
    COL_INDEX_MEM_VAL = 12

    COL_NAME_PC_SEL = "pc_sel"
    COL_NAME_ALUFUN = "AluFun"
    COL_NAME_OP2SEL = "Op2Sel"
    COL_NAME_OP1SEL = "Op1Sel"
    COL_NAME_WB_SEL = "wb_sel"
    COL_NAME_RF_WEN = "rf_wen"
    COL_NAME_MEM_RW = "mem_rw"
    COL_NAME_MEM_VAL = "mem_val"

    instr_ctrl_signals: dict

    instr_name: str

    _pc_sel = 0

    """
    Loads the control signals into
    the ControlSignals class field instr_ctrl_signals.
    """
    def load():
        ControlSignals.instr_ctrl_signals = {}

        csv_file = open(ControlSignals.CSV_FILENAME_CTRL_SIGNALS)
        csv_reader = csv.reader(csv_file)
        rows = []
        for row in csv_reader:
            rows.append(row)

        ControlSignals._set_high_impedance_to_neg_one(rows)
        
        for row_index in range(ControlSignals.ROW_INDEX_INSTR_BEGIN,
                               ControlSignals.ROW_INDEX_INSTR_END+1):
            row = rows[row_index]
            ControlSignals.instr_ctrl_signals[row[ControlSignals.COL_INDEX_INSTRUCTION].split(" ")[0].lower()] = {
                ControlSignals.COL_NAME_PC_SEL:row[ControlSignals.COL_INDEX_PC_SEL],
                ControlSignals.COL_NAME_ALUFUN:row[ControlSignals.COL_INDEX_ALUFUN],
                ControlSignals.COL_NAME_OP2SEL:row[ControlSignals.COL_INDEX_OP2SEL],
                ControlSignals.COL_NAME_OP1SEL:row[ControlSignals.COL_INDEX_OP1SEL],
                ControlSignals.COL_NAME_WB_SEL:row[ControlSignals.COL_INDEX_WB_SEL],
                ControlSignals.COL_NAME_RF_WEN:row[ControlSignals.COL_INDEX_RF_WEN],
                ControlSignals.COL_NAME_MEM_RW:row[ControlSignals.COL_INDEX_MEM_RW],
                ControlSignals.COL_NAME_MEM_VAL:row[ControlSignals.COL_INDEX_MEM_VAL]
            }

        _has_loaded_csv = True

    def set_instr_name(instr_name: str):
        if not ControlSignals._has_loaded_csv: ControlSignals.load()
        ControlSignals.instr_name = instr_name.lower()

    def set_pc_sel(pc_sel: int):
        ControlSignals._pc_sel = pc_sel

    def get_pc_sel():
        return ControlSignals._pc_sel

    get_alufun = lambda: ControlSignals.instr_ctrl_signals[
                             ControlSignals.instr_name
                         ][ControlSignals.COL_NAME_ALUFUN]
    get_op2sel = lambda: ControlSignals.instr_ctrl_signals[
                             ControlSignals.instr_name
                         ][ControlSignals.COL_NAME_OP2SEL]
    get_op1sel = lambda: ControlSignals.instr_ctrl_signals[
                             ControlSignals.instr_name
                         ][ControlSignals.COL_NAME_OP1SEL]
    get_wb_sel = lambda: ControlSignals.instr_ctrl_signals[
                             ControlSignals.instr_name
                         ][ControlSignals.COL_NAME_WB_SEL]
    get_rf_wen = lambda: ControlSignals.instr_ctrl_signals[
                             ControlSignals.instr_name
                         ][ControlSignals.COL_NAME_RF_WEN]
    get_mem_rw = lambda: ControlSignals.instr_ctrl_signals[
                             ControlSignals.instr_name
                         ][ControlSignals.COL_NAME_MEM_RW]
    get_mem_val = lambda: ControlSignals.instr_ctrl_signals[
                             ControlSignals.instr_name
                         ][ControlSignals.COL_NAME_MEM_VAL]
    
    def _set_high_impedance_to_neg_one(rows):
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                if rows[i][j] == "xx":
                    rows[i][j] = -1
                else: 
                    try:
                        rows[i][j] = int(rows[i][j],base=16)
                    except ValueError: pass
if __name__ == "__main__":
    ControlSignals.load()
    
