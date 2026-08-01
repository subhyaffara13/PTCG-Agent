
def error_inputs_unbind(op_info, device):
    make_arg = partial(make_tensor, dtype=torch.int32, device=device, requires_grad=False)
    yield ErrorInput(SampleInput(make_arg(()), args=(0,)), error_type=IndexError,
                     error_regex="Dimension specified as 0 but tensor has no dimensions")
    yield ErrorInput(SampleInput(make_arg((2,)), args=(2,)), error_type=IndexError,
                     error_regex="Dimension out of range")

