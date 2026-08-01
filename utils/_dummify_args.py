
def _dummify_args(_arg, var):
    dummy_dict = {}
    dummy_arg_list = []

    for arg in _arg:
        _s = Dummy()
        dummy_dict[_s] = var
        dummy_arg = arg.subs({var: _s})
        dummy_arg_list.append(dummy_arg)

    return dummy_arg_list, dummy_dict

