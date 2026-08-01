
def _conv_bn_add_root_node_getter_right(pattern):
    _add, _, bn_conv = pattern
    _bn, conv = bn_conv
    return conv

