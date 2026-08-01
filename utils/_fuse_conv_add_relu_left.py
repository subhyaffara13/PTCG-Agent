
def _fuse_conv_add_relu_left(is_qat, relu, add_pattern):
    add, conv, _ = add_pattern
    return nni.ConvAddReLU2d(conv, add, relu)

