
def fuse_linear_bn_eval(
    linear: LinearT,
    bn: torch.nn.modules.batchnorm._BatchNorm,
) -> LinearT:
    r"""Fuse a linear module and a BatchNorm module into a single, new linear module.

    Args:
        linear (torch.nn.Linear): A Linear module.
        bn (torch.nn.modules.batchnorm._BatchNorm): A BatchNorm module.

    Returns:
        torch.nn.Linear: The fused linear module.

    .. note::
        Both ``linear`` and ``bn`` must be in eval mode, and ``bn`` must have its running buffers computed.
    """
    if linear.training or bn.training:
        raise AssertionError("Fusion only for eval!")
    fused_linear = copy.deepcopy(linear)

    """
    Linear-BN needs to be fused while preserving the shapes of linear weight/bias.
    To preserve the shapes of linear weight/bias, the channel dim of bn needs to be broadcastable with the last dim of linear,
    because bn operates over the channel dim, (N, C_in, H, W) while linear operates over the last dim, (*, H_in).
    To be broadcastable, the number of features in bn and
    the number of output features from linear must satisfy the following condition:
    1. they are equal, or
    2. the number of features in bn is 1
    Otherwise, skip the folding path
    """
    if linear.out_features != bn.num_features and bn.num_features != 1:
        raise AssertionError(
            f"To fuse, linear.out_features == bn.num_features or bn.num_features == 1, "
            f"got linear.out_features={linear.out_features} and bn.num_features={bn.num_features}"
        )

    if bn.running_mean is None or bn.running_var is None:
        raise AssertionError("bn.running_mean and bn.running_var must not be None")
    fused_linear.weight, fused_linear.bias = fuse_linear_bn_weights(
        fused_linear.weight,
        fused_linear.bias,
        bn.running_mean,
        bn.running_var,
        bn.eps,
        bn.weight,
        bn.bias,
    )

    return fused_linear

