
def _register_model_output_pytree_node(output_type: type[ModelOutput]) -> None:
    if not _is_torch_available:
        return
    import torch

    # AMD CI runs PyTorch 2.8.0+rocm which does not support tracing `set.__contains__`
    # through TorchDynamo. Skip registration during compilation since the pytree node
    # is already registered from the preceding eager run.
    if torch.compiler.is_compiling():
        return
    if output_type in _registered_model_output_types:
        return

    import torch.utils._pytree as torch_pytree

    torch_pytree.register_pytree_node(
        output_type,
        _model_output_flatten,
        partial(_model_output_unflatten, output_type=output_type),
        serialized_type_name=f"{output_type.__module__}.{output_type.__name__}",
    )
    _registered_model_output_types.add(output_type)

