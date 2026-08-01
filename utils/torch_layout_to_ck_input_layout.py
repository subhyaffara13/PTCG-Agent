
def torch_layout_to_ck_input_layout(torch_layout):
    if V.graph.sizevars.statically_known_equals(torch_layout.stride[-1], 1):
        return "NGCHW"
    elif V.graph.sizevars.statically_known_equals(torch_layout.stride[-3], 1):
        return "NHWGC"
    else:
        return None

