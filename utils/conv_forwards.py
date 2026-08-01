
def conv_forwards(
    input: list[int],
    weight: list[int],
    bias: Optional[list[int]],
    stride: list[int],
    padding: list[int],
    dilation: list[int],
    transposed: bool,
    output_padding: list[int],
    groups: int,
) -> list[int]:
    has_dilation = len(dilation) > 0
    has_output_padding = len(output_padding) > 0
    dim = len(input)
    output_size: list[int] = []
    input_batch_size_dim = 0
    weight_output_channels_dim = 1 if transposed else 0
    output_size.append(input[input_batch_size_dim])
    if transposed:
        output_size.append(weight[weight_output_channels_dim] * groups)
    else:
        output_size.append(weight[weight_output_channels_dim])

    for d in range(2, dim):
        dilation_ = dilation[d - 2] if has_dilation else 1
        output_padding_ = output_padding[d - 2] if has_output_padding else 0
        if transposed:
            kernel = dilation_ * (weight[d] - 1)
            output_size.append(
                (input[d] - 1) * stride[d - 2]
                - 2 * padding[d - 2]
                + kernel
                + output_padding_
                + 1
            )
        else:
            kernel = dilation_ * (weight[d] - 1) + 1
            output_size.append(
                (input[d] + (2 * padding[d - 2]) - kernel) // stride[d - 2] + 1
            )
    return output_size

