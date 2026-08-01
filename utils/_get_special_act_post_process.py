
def _get_special_act_post_process(module: torch.nn.Module) -> Callable | None:
    r"""Get the special activation post process for `module`, this has
    higher priority than the activation post process in `qconfig`
    e.g.
    input: torch.nn.Sigmoid
    output: default_affine_fixed_qparam_fake_quant
    """
    return DEFAULT_MODULE_TO_ACT_POST_PROCESS.get(type_before_parametrizations(module))

