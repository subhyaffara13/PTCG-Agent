
def use_experts_implementation(
    experts_class: type[torch.nn.Module] | None = None,
    *,
    experts_interface: ExpertsInterface = ALL_EXPERTS_FUNCTIONS,
    is_concatenated: bool = True,
    is_transposed: bool = False,
    has_bias: bool = False,
    has_gate: bool = True,
) -> type[torch.nn.Module]:
    """Decorator to modify experts class to support different experts implementations.

    Args:
        experts_class (`type[torch.nn.Module]`, *optional*):
            The experts class to modify. If not provided, returns a decorator that can be applied to the class.
        experts_interface (`ExpertsInterface`, *optional*, defaults to `ALL_EXPERTS_FUNCTIONS`):
            The experts interface to use for dispatching the forward method.
        is_concatenated (`bool`, *optional*, defaults to `True`):
            Whether the expert weights are stored in concatenated layout [gate;up]
            or interleaved layout [gate0, up0, gate1, up1, ...].
        is_transposed (`bool`, *optional*, defaults to `False`):
            Whether the expert weights are stored in transposed format.
        has_bias (`bool`, *optional*, defaults to `False`):
            Whether the expert layers include bias terms or not.
        has_gate (`bool`, *optional*, defaults to `True`):
            Whether the experts use a gating mechanism or not.
            Whether it has gate_up_proj weights or just up_proj weights.

    Returns:
        `type[torch.nn.Module]`: The modified experts class.
    """

    def wrapper(experts_class: type[torch.nn.Module]) -> type[torch.nn.Module]:
        original_init = experts_class.__init__
        original_forward = experts_class.forward

        @wraps(original_init)
        def __init__(self, config, *args, **kwargs):
            original_init(self, config, *args, **kwargs)
            self.config = config
            self.has_gate = has_gate
            self.has_bias = has_bias
            self.is_transposed = is_transposed
            self.is_concatenated = is_concatenated

        @wraps(original_forward)
        def forward(self, *args, **kwargs):
            experts_forward = experts_interface.get_interface(self.config._experts_implementation, original_forward)
            return experts_forward(self, *args, **kwargs)

        if not hasattr(experts_class, "_apply_gate"):
            experts_class._apply_gate = _default_apply_gate

        experts_class.__init__ = __init__
        experts_class.forward = forward
        return experts_class

    if experts_class is not None:
        return wrapper(experts_class)

    return wrapper

