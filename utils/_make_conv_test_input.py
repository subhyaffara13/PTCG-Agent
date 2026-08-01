
def _make_conv_test_input(
    batch_size,
    in_channels_per_group,
    input_feature_map_size,
    out_channels_per_group,
    groups,
    kernel_size,
    X_scale,
    X_zero_point,
    W_scale,
    W_zero_point,
    use_bias,
    use_channelwise,
):
    in_channels = in_channels_per_group * groups
    out_channels = out_channels_per_group * groups

    (X_value_min, X_value_max) = (0, 4)
    X_init = torch.randint(
        X_value_min,
        X_value_max,
        (
            batch_size,
            in_channels,
        )
        + input_feature_map_size,
    )
    X = X_scale * (X_init - X_zero_point).float()
    X_q = torch.quantize_per_tensor(
        X, scale=X_scale, zero_point=X_zero_point, dtype=torch.quint8
    )

    W_scale = W_scale * out_channels
    W_zero_point = W_zero_point * out_channels
    # Resize W_scale and W_zero_points arrays equal to out_channels
    W_scale = W_scale[:out_channels]
    W_zero_point = W_zero_point[:out_channels]
    # For testing, we use small values for weights and for activations so that
    # no overflow occurs in vpmaddubsw instruction. If the overflow occurs in
    # qconv implementation and if there is no overflow.
    # In reference we can't exactly match the results with reference.
    # Please see the comment in qconv implementation file
    #   aten/src/ATen/native/quantized/cpu/qconv.cpp for more details.
    (W_value_min, W_value_max) = (-5, 5)
    # The operator expects them in the format
    # (out_channels, in_channels/groups,) + kernel_size
    W_init = torch.randint(
        W_value_min,
        W_value_max,
        (
            out_channels,
            in_channels_per_group,
        )
        + kernel_size,
    )
    b_init = torch.randint(0, 10, (out_channels,))

    if use_channelwise:
        W_shape = (-1, 1) + (1,) * len(kernel_size)
        W_scales_tensor = torch.tensor(W_scale, dtype=torch.float)
        W_zero_points_tensor = torch.tensor(W_zero_point, dtype=torch.float)
        W = (
            W_scales_tensor.reshape(*W_shape)
            * (W_init.float() - W_zero_points_tensor.reshape(*W_shape)).float()
        )
        b = X_scale * W_scales_tensor * b_init.float()
        W_q = torch.quantize_per_channel(
            W,
            W_scales_tensor.double(),
            W_zero_points_tensor.long(),
            0,
            dtype=torch.qint8,
        )
    else:
        W = W_scale[0] * (W_init - W_zero_point[0]).float()
        b = X_scale * W_scale[0] * b_init.float()
        W_q = torch.quantize_per_tensor(
            W, scale=W_scale[0], zero_point=W_zero_point[0], dtype=torch.qint8
        )

    return (X, X_q, W, W_q, b if use_bias else None)

