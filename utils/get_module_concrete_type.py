
def get_module_concrete_type(nn_module, share_types=True):
    """
    Get a concrete type for nn_modules.

    If share_types is True, the concrete type is fetched from concrete_type_store.
    If it is False, a new concrete type is created without first searching concrete_type_store.

    Args:
        nn_module:  The original Python nn.Module that we are creating a ScriptModule for.
        share_types = Whether to share underlying JIT types between modules (if possible).

    Returns:
        A concrete type for nn_module.
    """
    if not isinstance(nn_module, Module):
        raise AssertionError(f"Expected Module, got {type(nn_module)}")
    if isinstance(nn_module, torch.jit.ScriptModule) and hasattr(
        nn_module, "_concrete_type"
    ):
        return nn_module._concrete_type

    if share_types:
        # Look into the store of cached JIT types
        concrete_type = concrete_type_store.get_or_create_concrete_type(nn_module)
    else:
        # Get a concrete type directly, without trying to reuse an existing JIT
        # type from the type store.
        concrete_type_builder = infer_concrete_type_builder(nn_module, share_types)
        concrete_type_builder.set_poisoned()
        concrete_type = concrete_type_builder.build()

    return concrete_type

