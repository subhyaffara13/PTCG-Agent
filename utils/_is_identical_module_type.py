
def _is_identical_module_type(mod1, mod2):
    # Compare if two modules have the same dtype
    mod1_module_types = [type(mod) for mod in mod1.modules()]
    mod2_module_types = [type(mod) for mod in mod2.modules()]
    return mod1_module_types == mod2_module_types

