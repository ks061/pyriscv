class Counters:
    counter_dict = None
    
    def __init__():
        Counters.reset()

    def get(category, counter):
        if Counters.counter_dict == None: Counters.__init__()

        return Counters.counter_dict[category][counter]

    def increment(category, counter=None):
        if Counters.counter_dict == None: Counters.__init__()

        if counter == None: Counters.counter_dict[category] = Counters.counter_dict[category] + 1
        else: Counters.counter_dict[category][counter] = Counters.counter_dict[category][counter] + 1

    def add(category, counter=None, entity=None):
        if Counters.counter_dict == None: Counters.__init__()

        if counter == None: Counters.counter_dict[category].append(entity)
        else: Counters.counter_dict[category][counter].append(entity)

    def __str__():
        return str(Counters.counter_dict)

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
