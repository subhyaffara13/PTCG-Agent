
def _conv_add_relu_root_node_getter_right(pattern):
    _relu, add_pattern = pattern
    _, _extra_input, conv = add_pattern
    return conv

