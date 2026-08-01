
def get_nn_mod_test_name(**kwargs):
    if 'fullname' in kwargs:
        test_name = kwargs['fullname']
    else:
        test_name = get_nn_module_name_from_kwargs(**kwargs)
        if 'desc' in kwargs:
            test_name = f"{test_name}_{kwargs['desc']}"
    return f'test_nn_{test_name}'

