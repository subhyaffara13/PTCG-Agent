
def torch_layout_to_ck_output_layout(torch_layout):
    if V.graph.sizevars.statically_known_equals(torch_layout.stride[-1], 1):
        return "NGKHW"
    elif V.graph.sizevars.statically_known_equals(torch_layout.stride[-3], 1):
        return "NHWGK"
    else:
        return None

