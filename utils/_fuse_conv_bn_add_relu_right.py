
def _fuse_conv_bn_add_relu_right(is_qat, relu, add_pattern):
    add, _, bn_conv = add_pattern
    bn, conv = bn_conv
    if is_qat:
        raise NotImplementedError(f"Cannot fuse train modules: {(conv, bn, add, relu)}")
    else:
        fused_conv = nn.utils.fusion.fuse_conv_bn_eval(conv, bn)
        return nni.ConvAddReLU2d(fused_conv, add, relu)

