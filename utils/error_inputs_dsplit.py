
def error_inputs_dsplit(op_info, device, **kwargs):
    make_arg = partial(make_tensor, dtype=torch.float32, device=device)
    err_msg1 = ("torch.dsplit requires a tensor with at least 3 dimension, "
                "but got a tensor with 1 dimensions!")
    yield ErrorInput(SampleInput(make_arg(S), 0), error_regex=err_msg1)

    err_msg2 = (f"torch.dsplit attempted to split along dimension 2, "
                f"but the size of the dimension {S} "
                f"is not divisible by the split_size 0!")
    yield ErrorInput(SampleInput(make_arg(S, S, S), 0), error_regex=err_msg2)

