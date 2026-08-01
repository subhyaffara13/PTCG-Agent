
def torch_layout_to_ck_layouts(torch_layout):
    # logically, torch tensors are always NCHW,
    # and channels-last memory layout is visible in the strides
    if V.graph.sizevars.statically_known_equals(torch_layout.stride[-1], 1):
        # when input or output is NCHW
        # NB: torch.conv2d result is always NCHW
        return ["NGCHW", "GKCYX", "NGKHW"]
    elif V.graph.sizevars.statically_known_equals(torch_layout.stride[-3], 1):
        # when input or output or weight is channels-last
        return ["NHWGC", "GKYXC", "NHWGK"]
    else:
        return None

