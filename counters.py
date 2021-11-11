import json

class Counters:
    counter_dict = None
    
    def __init__():
        Counters.reset()

    def get(category, counter):
        if Counters.counter_dict == None: Counters.__init__()

        return Counters.counter_dict[category][counter]

    def increment(category, counter=None, amount=1):
        if Counters.counter_dict == None: Counters.__init__()

        if counter == None: Counters.counter_dict[category] = Counters.counter_dict[category] + amount
        else: Counters.counter_dict[category][counter] = Counters.counter_dict[category][counter] + amount

    def add(category, counter=None, entity=None):
        if Counters.counter_dict == None: Counters.__init__()

        if entity not in Counters.counter_dict[category][counter]:
            Counters.counter_dict[category][counter].append(entity)

    def _calc_pcts():
        # calc branch pcts
        total_branch_forward = \
            Counters.counter_dict["branch"]["forward_taken"] + \
            Counters.counter_dict["branch"]["forward_not_taken"]
        Counters.counter_dict["branch"]["forward_pct_taken"] = str(round(\
            Counters.counter_dict["branch"]["forward_taken"] * 100 / \
            total_branch_forward, 2)) + "%"
        Counters.counter_dict["branch"]["forward_pct_not_taken"] = str(round(\
            Counters.counter_dict["branch"]["forward_not_taken"] * 100 / \
            total_branch_forward, 2)) + "%"
        total_branch_backward = \
            Counters.counter_dict["branch"]["backward_taken"] + \
            Counters.counter_dict["branch"]["backward_not_taken"]
        Counters.counter_dict["branch"]["backward_pct_taken"] = str(round(\
            Counters.counter_dict["branch"]["backward_taken"] * 100 / \
            total_branch_backward, 2)) + "%"
        Counters.counter_dict["branch"]["backward_pct_not_taken"] = str(round(\
            Counters.counter_dict["branch"]["backward_not_taken"] * 100 / \
            total_branch_backward, 2)) + "%"

        # calc arithmetic pcts
        total_inst_count = 0
        for key in Counters.counter_dict["inst_count"].keys():
            total_inst_count += Counters.counter_dict["inst_count"][key]
        
        # save current inst_count keys before new ones are added
        inst_count_keys = [key for key in Counters.counter_dict["inst_count"].keys()]
        for key in inst_count_keys:
            Counters.counter_dict["inst_count"][key + "_pct"] = str(round(\
            Counters.counter_dict["inst_count"][key] * 100 / \
            total_inst_count, 2)) + "%"

    def __str__():
        Counters._calc_pcts()
        return "------------------------------<      Counters      >------------------------------\n" + str(json.dumps(Counters.counter_dict, indent=4))

    def reset():
        Counters.counter_dict = {
            # categories  # counters
            "branch": {
                          "forward_taken": 0,
                          "backward_not_taken": 0,
                          "backward_taken": 0,
                          "forward_not_taken": 0    
                      },
            "inst_count": {
                              "arithmetic": 0,
                              "csr": 0,
                              "branch": 0,
                              "jump": 0,
                              "store": 0,
                              "jump_reg": 0,
                              "load": 0,
                              "misc": 0
                          },
            "inst_name": {
                             "arithmetic": [],
                             "csr": [],
                             "branch": [],
                             "jump": [],
                             "store": [],
                             "jump_reg": [],
                             "load": [],
                             "misc": []
                         },
            "inst_fetch_bytes": 0,
            "mcycle": 0,
            "mem_write_bytes": 0,
            "mem_read_bytes": 0
        }    
