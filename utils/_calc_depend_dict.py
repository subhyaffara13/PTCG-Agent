
def _calc_depend_dict(vars):
    names = list(vars.keys())
    depend_dict = {}
    for n in names:
        _get_depend_dict(n, vars, depend_dict)
    return depend_dict

