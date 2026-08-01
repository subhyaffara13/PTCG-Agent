
def constrain_conv_to_fx_strides(fx_node, *args, **kwargs):
    assert fx_node.target is torch.ops.aten.convolution.default
    if V.graph.layout_opt:
        return args, kwargs
    else:
        return constrain_to_fx_strides(fx_node, *args, **kwargs)

