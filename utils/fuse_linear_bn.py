
def fuse_linear_bn(is_qat, linear, bn):
    r"""Return the fused linear and bn modules.
    Given the linear and bn modules, fuses them and returns the fused module

    Args:
        is_qat: a flag for whether we are using quantization aware training fusion
        or post training quantization fusion
        linear: Module instance of type Linear
        bn: BatchNorm1d instance that needs to be fused with the linear layer

    Examples::

        >>> m1 = nn.Linear(20, 10)
        >>> b1 = nn.BatchNorm1d(10)
        >>> # xdoctest: +SKIP
        >>> m2 = fuse_linear_bn(m1, b1)
    """
    if linear.training != bn.training:
        raise AssertionError(
            "Linear and BN both must be in the same mode (train or eval)."
        )

    if is_qat:
        if bn.num_features != linear.out_features:
            raise AssertionError(
                "Output features of Linear must match num_features of BatchNorm1d"
            )
        if not bn.affine:
            raise AssertionError(
                "Only support fusing BatchNorm1d with affine set to True"
            )
        if not bn.track_running_stats:
            raise AssertionError(
                "Only support fusing BatchNorm1d with tracking_running_stats set to True"
            )
        return nni.LinearBn1d(linear, bn)
    else:
        return nn.utils.fusion.fuse_linear_bn_eval(linear, bn)

