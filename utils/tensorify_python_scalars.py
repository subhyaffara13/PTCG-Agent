import os

def tensorify_python_scalars(
    gm: GraphModule, shape_env: ShapeEnv, fake_mode: fake_tensor.FakeTensorMode
) -> None:
    """
    Converts Python scalar operations into Tensor operations within the graph. This pass looks for
    Tensor operations that involve SymFloat arguments and transforms them into equivalent operations
    that use only Tensor inputs.

    Args:
        gm: The FX graph module representing the computation graph.
        shape_env: The shape environment responsible for symbolic shape tracking and propagation
        during graph transformations.

    Returns:
        None
    """

    knob = True
    if (env := os.getenv("TENSORIFY_PYTHON_SCALARS")) is not None:
        if env in ("0", "FALSE"):
            knob = False
    else:
        knob = justknobs_check("pytorch/compiler:tensorify_python_scalars")
    if not knob:
        return None

    # This pass uses MetaProxy which relies on __torch_function__.
    # DisableTorchFunctionSubclass may be active here (see #177088),
    # so re-enable dispatch for MetaProxy ops.
    with torch._C._EnableTorchFunction():
        return _tensorify_impl(gm, shape_env, fake_mode)

