
def handle_noncontiguous_outputs(input_tlist, output):
    device = None
    from torch._subclasses.fake_tensor import FakeTensor

    for t in input_tlist:
        if isinstance(t, FakeTensor):
            device = t.fake_device
            break

    if not is_noncontiguous_supported(device):
        output = output.contiguous()

    return output

