from pydigital.utils import sextend

class BranchCondGen:
    _br_eq = False
    _br_lt = False
    _br_ltu = False

    def reset():
        BranchCondGen._br_eq = False
        BranchCondGen._br_lt = False
        BranchCondGen._br_ltu = False

    def set_branch_conds(rs1_val, rs2_val):
        BranchCondGen.reset()
        if rs1_val == None: 
            BranchCondGen.reset()
            return
        if rs2_val == None: 
            BranchCondGen.reset()
            return
        if rs1_val == rs2_val: BranchCondGen._br_eq = True
        if rs1_val < rs2_val: BranchCondGen._br_lt = True
        if abs(rs1_val) < abs(rs2_val): BranchCondGen._br_ltu = True

    get_br_eq = lambda: BranchCondGen._br_eq
    get_br_lt = lambda: BranchCondGen._br_lt
    get_br_ltu = lambda: BranchCondGen._br_ltu