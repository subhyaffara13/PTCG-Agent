
def error_inputs_fftn(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)
    # Specifying a dimension on a zero-dimensional tensor
    yield ErrorInput(
        SampleInput(make_arg(), dim=(0,)),
        error_type=IndexError,
        error_regex="Dimension specified as 0 but tensor has no dimensions",
    )

