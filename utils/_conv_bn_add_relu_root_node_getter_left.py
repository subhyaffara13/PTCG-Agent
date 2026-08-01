
def _conv_bn_add_relu_root_node_getter_left(pattern):
    _relu, add_pattern = pattern
    _, bn_conv, _ = add_pattern
    _bn, conv = bn_conv
    return conv

