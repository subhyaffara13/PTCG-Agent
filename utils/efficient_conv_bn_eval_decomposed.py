
def efficient_conv_bn_eval_decomposed(
    bn_weight,
    bn_bias,
    bn_running_mean,
    bn_running_var,
    bn_eps,
    conv: torch._ops.OpOverload,
    conv_weight,
    conv_bias,
    x,
    conv_remaining_args,
):
    """
    Implementation based on https://arxiv.org/abs/2305.11624
    "Efficient ConvBN Blocks for Transfer Learning and Beyond"
    It leverages the associative law between convolution and affine transform,
    i.e., normalize (weight conv feature) = (normalize weight) conv feature.
    It works for Eval mode of ConvBN blocks during validation, and can be used
    for **training** as well, but only if one sets `bn.training=False`. It
     reduces memory footprint and computation cost, at the cost of slightly
     reduced numerical stability.
    Args:
    """
    assert bn_running_var is not None

    # These lines of code are designed to deal with various cases
    # like bn without affine transform, and conv without bias
    weight_on_the_fly = conv_weight
    if conv_bias is not None:
        bias_on_the_fly = conv_bias
    else:
        bias_on_the_fly = torch.zeros_like(bn_running_var)

    if bn_weight is None:
        bn_weight = torch.ones_like(bn_running_var)

    if bn_bias is None:
        bn_bias = torch.zeros_like(bn_running_var)

    # shape of [C_out, 1, 1, 1] in Conv2d
    target_shape = [-1] + [1] * (conv_weight.ndim - 1)
    if "conv_transpose" in conv.__str__():
        # for transposed conv, the C_out dimension should at index 1.
        target_shape[:2] = [target_shape[1], target_shape[0]]
    weight_coeff = torch.rsqrt(bn_running_var + bn_eps).reshape(target_shape)
    # shape of [C_out, 1, 1, 1] in Conv2d
    coefff_on_the_fly = bn_weight.view_as(weight_coeff) * weight_coeff

    # shape of [C_out, C_in, k, k] in Conv2d
    weight_on_the_fly = weight_on_the_fly * coefff_on_the_fly
    # shape of [C_out] in Conv2d
    bias_on_the_fly = bn_bias + coefff_on_the_fly.flatten() * (
        bias_on_the_fly - bn_running_mean
    )

    input = x
    return conv(*((input, weight_on_the_fly, bias_on_the_fly) + conv_remaining_args))

