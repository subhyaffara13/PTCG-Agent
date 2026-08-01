
def error_inputs_hsplit(op_info, device, **kwargs):
    make_arg = partial(make_tensor, dtype=torch.float32, device=device)
    err_msg1 = ("torch.hsplit requires a tensor with at least 1 dimension, "
                "but got a tensor with 0 dimensions!")
    yield ErrorInput(SampleInput(make_arg(()), 0), error_regex=err_msg1)

    err_msg2 = (f"torch.hsplit attempted to split along dimension 1, "
                f"but the size of the dimension {S} "
                f"is not divisible by the split_size 0!")
    yield ErrorInput(SampleInput(make_arg((S, S, S)), 0), error_regex=err_msg2)

    # Incorrect type for indices_or_section argument
    err_msg3 = ("received an invalid combination of arguments.")
    yield ErrorInput(
        SampleInput(make_arg((S, S, S)), "abc"),
        error_type=TypeError, error_regex=err_msg3)

