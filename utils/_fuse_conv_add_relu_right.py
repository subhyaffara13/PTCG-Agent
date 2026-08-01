
def _fuse_conv_add_relu_right(is_qat, relu, add_pattern):
    add, _, conv = add_pattern
    return nni.ConvAddReLU2d(conv, add, relu)

