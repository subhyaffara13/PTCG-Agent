
def get_sorted_names(vars):
    depend_dict = _calc_depend_dict(vars)
    names = []
    for name in list(depend_dict.keys()):
        if not depend_dict[name]:
            names.append(name)
            del depend_dict[name]
    while depend_dict:
        for name, lst in list(depend_dict.items()):
            new_lst = [n for n in lst if n in depend_dict]
            if not new_lst:
                names.append(name)
                del depend_dict[name]
            else:
                depend_dict[name] = new_lst
    return [name for name in names if name in vars]

