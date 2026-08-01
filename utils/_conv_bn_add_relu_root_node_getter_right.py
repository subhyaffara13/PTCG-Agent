
def _conv_bn_add_relu_root_node_getter_right(pattern):
    _relu, add_pattern = pattern
    _, _, bn_conv = add_pattern
    _bn, conv = bn_conv
    return conv

