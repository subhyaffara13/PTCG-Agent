
def _fuse_conv_add_left(is_qat, add, conv, _):
    return nni.ConvAdd2d(conv, add)

