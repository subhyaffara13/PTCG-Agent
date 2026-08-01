
def get_nn_module_class_from_kwargs(**kwargs):
    name = get_nn_module_name_from_kwargs(**kwargs)
    index = name.find("_")
    if index == -1:
        return name
    else:
        return name[0:name.find("_")]

