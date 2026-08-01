
def error_inputs_roll(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)
    err_msg1 = "`shifts` required"
    s1 = SampleInput(make_arg((S,)), ())
    yield ErrorInput(s1, error_regex=err_msg1)

    err_msg2 = ("shifts and dimensions must align")
    s2 = SampleInput(make_arg((S, S)), (2, 1), 0)
    yield ErrorInput(s2, error_regex=err_msg2)

    err_msg3 = ("out of range")
    s3 = SampleInput(make_arg((S, )), 0, 2)
    yield ErrorInput(s3, error_regex=err_msg3, error_type=IndexError)

    err_msg4 = ("Dimension specified as 0")
    s4 = SampleInput(make_arg(()), 0, 0)
    yield ErrorInput(s4, error_regex=err_msg4, error_type=IndexError)

