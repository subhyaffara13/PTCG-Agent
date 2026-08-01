
def _load_sonicmoe_kernel() -> SonicMoE:
    """
    Load sonic-moe once and return its entry points.

    Raises `ImportError` if CUDA/hardware requirements are not met, or if the kernel or
    required symbols are not found.
    """

    if not torch.cuda.is_available():
        raise ImportError(
            "sonic-moe kernel requires CUDA, but CUDA is not available. Use a different `experts_implementation`."
        )

    # sonic-moe requires Hopper (SM90) or newer
    major = torch.cuda.get_device_capability()[0]
    if major < 9:
        raise ImportError(
            f"sonic-moe requires a Hopper (SM90+) or newer GPU, but the current device "
            f"has compute capability {major}.x. Use a different `experts_implementation`."
        )

    kernel = lazy_load_kernel("sonic-moe")
    if kernel is None:
        raise ImportError(
            "Failed to load the sonic-moe kernel — check that `kernels-community/sonic-moe` "
            "has a build matching the current torch/CUDA."
        )

    activation_type_enum = getattr(getattr(kernel, "enums", None), "ActivationType", None)
    moe_general_routing_inputs = getattr(kernel, "moe_general_routing_inputs", None)

    missing = [
        name
        for name, attr in [
            ("enums.ActivationType", activation_type_enum),
            ("moe_general_routing_inputs", moe_general_routing_inputs),
        ]
        if attr is None
    ]
    if missing:
        raise ImportError(
            f"sonic-moe kernel is missing required symbols: {', '.join(missing)}. "
            "Make sure you have the `kernels` package and `nvidia-cutlass-dsl` installed."
        )

    return SonicMoE(
        activation_type_enum=activation_type_enum,
        moe_general_routing_inputs=moe_general_routing_inputs,
    )

