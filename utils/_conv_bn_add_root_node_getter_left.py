
def _conv_bn_add_root_node_getter_left(add_pattern):
    _, bn_conv, _ = add_pattern
    _bn, conv = bn_conv
    return conv

