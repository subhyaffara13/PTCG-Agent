
def freeze_bn_stats(mod):
    if type(mod) in {
        ConvBnReLU1d,
        ConvBnReLU2d,
        ConvBnReLU3d,
        ConvBn1d,
        ConvBn2d,
        ConvBn3d,
    }:
        mod.freeze_bn_stats()

