
def fuse_convtranspose_bn(is_qat, convt, bn):
    r"""Return the fused ConvTranspose and bn modules.
    Given ConvTranspose and bn modules, fuses them and returns the fused module

    Args:
        convt: Module instance of type ConvTransposeNd
        bn: BatchNormNd instance that needs to be fused with the linear layer.
            batch norm N should match the ConvTranspose N

    Examples::

        >>> m1 = nn.ConvTranspose2d(10, 20, 3)
        >>> b1 = nn.BatchNorm2d(20)
        >>> # xdoctest: +SKIP
        >>> m2 = fuse_convtranspose_bn(m1, b1)
    """
    if convt.training != bn.training:
        raise AssertionError(
            "ConvTranspose and BN both must be in the same mode (train or eval)."
        )

    if is_qat:
        raise Exception(  # noqa: TRY002
            "Fusing ConvTranspose+BatchNorm not yet supported in QAT."
        )
    else:
        return nn.utils.fusion.fuse_conv_bn_eval(convt, bn, transpose=True)

