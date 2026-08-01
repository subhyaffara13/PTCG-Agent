
def is_get_tensor_info_node(node):
    return node.op == "call_method" and node.target in ["shape", "size"]

