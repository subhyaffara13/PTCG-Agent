
def add_tensor_parallel_hooks_to_module(
    model,
    module,
    current_module_plan,
    layer_name,
    device_mesh,
):
    r"""
    This function is called in `PretrainedModel.post_init()`. It is responsible of adding hooks
    to the modules of the `model`, based on the `PretrainedModel._tp_plan`.

    This is the place where we add the `pre_forward` and `post_forwards` hooks. These are defined
    for each `TensorParallelLayer` as `_prepare_input_fn` and `_prepare_output_fn`.

    Args:
        model (`PretrainedModel`): The model containing the modules.
        module (`nn.Module`): The current module to which we want to add the hooks.
        current_module_plan (`str` or `None`): The tensor parallel plan for the current module, if any.
        layer_name (`str`): The qualified name of the current module.
        device_mesh (`dist.device_mesh.DeviceMesh`): The device mesh for distributed communication.

    """
    if current_module_plan is not None:
        tp_layer = ALL_PARALLEL_STYLES[current_module_plan]
        try:
            tp_layer.prepare_module_tp(module, device_mesh, config=model.config)
        except NotImplementedError as e:
            logger.warning(
                f"Trying to prepare {layer_name}, but it's not supported. Corresponding module: {module} Fix it's TP "
                f"plan: {e}"
            )

        module._hf_tp_plan = current_module_plan
        module._hf_device_mesh = device_mesh
        module.__repr__ = lambda: f"{module.__repr__()}\nTP Plan: {current_module_plan}"

