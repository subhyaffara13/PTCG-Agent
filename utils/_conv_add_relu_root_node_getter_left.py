
def _conv_add_relu_root_node_getter_left(pattern):
    _relu, add_pattern = pattern
    _, conv, _ = add_pattern
    return conv

