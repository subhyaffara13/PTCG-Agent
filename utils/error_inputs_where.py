
def error_inputs_where(op_info, device, **kwargs):
    shape = (S,)
    err_msg = "Expected all tensors to be on the same device"
    for devices in product(('cpu', device), repeat=3):
        if len(set(devices)) == 2:
            si = SampleInput(make_tensor(shape, device=devices[0], dtype=torch.float32),
                             args=(make_tensor(shape, dtype=torch.bool, device=devices[1]),
                             make_tensor(shape, device=devices[2], dtype=torch.float32)))
            yield ErrorInput(si, error_regex=err_msg)

