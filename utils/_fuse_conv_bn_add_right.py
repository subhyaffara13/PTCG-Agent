
def _fuse_conv_bn_add_right(is_qat, add, _, bn_conv):
    bn, conv = bn_conv
    if is_qat:
        raise NotImplementedError(f"Cannot fuse train modules: {(conv, bn, add)}")
    else:
        fused_conv = nn.utils.fusion.fuse_conv_bn_eval(conv, bn)
        return nni.ConvAdd2d(fused_conv, add)

