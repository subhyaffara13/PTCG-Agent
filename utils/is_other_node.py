
def is_other_node(node, modules):
    func_list = [
        torch.cat,
    ]
    method_list: list[Any] = []
    module_type_list: list[Any] = []
    return _is_node_in_list(node, modules, func_list, method_list, module_type_list)

