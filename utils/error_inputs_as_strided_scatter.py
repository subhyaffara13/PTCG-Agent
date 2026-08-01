
def error_inputs_as_strided_scatter(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32, requires_grad=False)

    # Create a small tensor and try to scatter it out of bounds
    input_t = make_arg([4, 4])
    input_src = make_arg([2, 2])
    yield ErrorInput(
        SampleInput(input_t, input_src, [2, 2], [200, 200], storage_offset=0),
        error_regex="itemsize 4 requiring a storage size of 1604 are out of bounds for storage of size 64"
    )

