
def fused_module_supports_equalization(module) -> bool:
    """Checks if the fused node supports equalization."""
    return type(module) in [
        nni.LinearReLU,
        nni.ConvReLU1d,
        nni.ConvReLU2d,
        nni.ConvReLU3d,
    ]

