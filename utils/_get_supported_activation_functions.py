
def _get_supported_activation_functions():
    SUPPORTED_ACTIVATION_FUNCTIONS = {
        F.relu,
        F.rrelu,
        F.hardtanh,
        F.relu6,
        F.sigmoid,
        F.hardsigmoid,
        F.tanh,
        F.silu,
        F.mish,
        F.hardswish,
        F.elu,
        F.celu,
        F.selu,
        F.hardshrink,
        F.leaky_relu,
        F.logsigmoid,
        F.softplus,
        F.prelu,
        F.softsign,
        F.tanhshrink,
        F.gelu,
    }
    return SUPPORTED_ACTIVATION_FUNCTIONS

