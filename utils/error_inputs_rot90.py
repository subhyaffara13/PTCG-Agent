
def error_inputs_rot90(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)
    err_msg1 = "expected total rotation dims"
    s1 = SampleInput(make_arg((S, S)), dims=(0,))
    yield ErrorInput(s1, error_regex=err_msg1)

    err_msg2 = "expected total dims >= 2"
    s2 = SampleInput(make_arg((S,)))
    yield ErrorInput(s2, error_regex=err_msg2)

    err_msg3 = "expected rotation dims to be different"
    s3 = SampleInput(make_arg((S, S)), dims=(1, 1))
    yield ErrorInput(s3, error_regex=err_msg3)

