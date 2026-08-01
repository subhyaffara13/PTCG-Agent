
def get_nn_module_name_from_kwargs(**kwargs):
    if 'module_name' in kwargs:
        return kwargs['module_name']
    elif 'fullname' in kwargs:
        return kwargs['fullname']
    elif 'constructor' in kwargs:
        return kwargs['constructor'].__name__

