
def _is_node_in_list(node, modules, func_list, method_list, module_type_list):
    is_call_function = node.op == "call_function" and node.target in func_list
    is_call_method = node.op == "call_method" and node.target in method_list
    is_call_module = (
        node.op == "call_module" and type(modules[str(node.target)]) in module_type_list
    )
    return is_call_function, is_call_method, is_call_module

