
def is_special_pattern_node(node, modules):
    res_function, res_method, res_module = False, False, False
    for checker in [
        is_fixed_qparams_node,
        is_default_node,
        is_copy_node,
        is_general_tensor_shape_node,
        is_other_node,
    ]:
        is_call_function, is_call_method, is_call_module = checker(node, modules)
        res_function = res_function or is_call_function
        res_method = res_method or is_call_method
        res_module = res_module or is_call_module
    return res_function, res_method, res_module

