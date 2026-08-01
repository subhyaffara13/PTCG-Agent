
def error_inputs_mean(op_info, device, is_ref=False, **kwargs):
    if is_ref:
        err_msg1 = (r"mean\(\): could not infer output dtype. "
                    r"Input dtype must be either a floating point or complex dtype. "
                    r"Got: torch.int64")
    else:
        err_msg1 = (r"mean\(\): could not infer output dtype. "
                    r"Input dtype must be either a floating point or complex dtype. "
                    r"Got: Long")
    yield ErrorInput(
        SampleInput(make_tensor((3, 4, 5), dtype=torch.int64, device=device), []),
        error_regex=err_msg1,
    )

    if is_ref:
        err_msg2 = (r"mean\(\): could not infer output dtype. "
                    r"Optional dtype must be either a floating point or complex dtype. "
                    r"Got: torch.int64")
    else:
        err_msg2 = (r"mean\(\): could not infer output dtype. "
                    r"Optional dtype must be either a floating point or complex dtype. "
                    r"Got: Long")
    yield ErrorInput(
        SampleInput(
            make_tensor((3, 4, 5), dtype=torch.float32, device=device),
            [],
            dtype=torch.int64),
        error_regex=err_msg2
    )

