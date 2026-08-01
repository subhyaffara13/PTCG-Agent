
def make_named_value_info(name):
    vi = onnx.ValueInfoProto()
    vi.name = name
    return vi

