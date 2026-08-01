
def error_inputs_sum_to_size(op_info, device, **kwargs):
    shape = (M, S, M)
    err_msg = "is not expandable to size"
    si = SampleInput(make_tensor(shape, device=device, dtype=torch.float32), args=(M, M))
    yield ErrorInput(si, error_regex=err_msg)

    shape = (M + 1, S, S, M)
    err_msg = "is not expandable to size"
    si = SampleInput(make_tensor(shape, device=device, dtype=torch.float32), args=(M + 1, 1))
    yield ErrorInput(si, error_regex=err_msg)

