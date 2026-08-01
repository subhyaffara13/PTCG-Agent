
def upsample_common_check(input_size, output_size, num_spatial_dims):
    torch._check(
        len(output_size) == num_spatial_dims,
        lambda: f"It is expected output_size equals to {num_spatial_dims}, but got size {len(output_size)}",
    )
    expected_input_dims = num_spatial_dims + 2  # N, C, ...
    torch._check(
        len(input_size) == expected_input_dims,
        lambda: f"It is expected input_size equals to {expected_input_dims}, but got size {len(input_size)}",
    )

    torch._check(
        all(s > 0 for s in input_size[2:]) and all(s > 0 for s in output_size),
        lambda: f"Input and output sizes should be greater than 0, but got "
        f"input size {input_size} and output size {output_size}",
    )

    nbatch, channels = input_size[:2]
    return (nbatch, channels, *output_size)

