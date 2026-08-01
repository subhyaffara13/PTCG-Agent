
def is_getattr_tensor_metadata_node(node):
    return (
        node.op == "call_function"
        and node.target is getattr
        and node.args[1] == "shape"
    )

