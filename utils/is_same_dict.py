
def is_same_dict(inductor_dict, optimus_dict):
    for pass_name, count in optimus_dict.items():
        if count != dict(inductor_dict).get(pass_name, 0):
            return False
    return True

