
def _fuse_conv_add_right(is_qat, add, _, conv):
    return nni.ConvAdd2d(conv, add)

