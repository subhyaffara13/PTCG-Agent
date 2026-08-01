
def load_offloaded_parameter(model: "PreTrainedModel", param_name: str) -> torch.Tensor:
    """Load `param_name` from disk, if it was offloaded due to the device_map, and thus lives as a meta parameter
    inside `model`.
    This is needed when resaving a model, when some parameters were offloaded (we need to load them from disk, to
    then resave them to disk in the correct shard...)."""
    # Start from the most inner module, and try to find the hook that was used for offloading the param
    module_parts = param_name.split(".")
    modules_to_check = [".".join(module_parts[:-idx]) for idx in range(1, len(module_parts))] + [""]
    for parent_name in modules_to_check:
        parent = model.get_submodule(parent_name)
        if hasattr(parent, "_hf_hook"):
            weights_map = parent._hf_hook.weights_map
            truncated_param_name = param_name.replace(f"{parent_name}." if parent_name != "" else parent_name, "")
            break
    # If we did not break the loop, something is wrong
    else:
        raise ValueError(
            f"{param_name} is on the meta device because it was offloaded, but we could not find "
            "the corresponding hook for it"
        )

    # This call loads it from disk
    tensor = weights_map[truncated_param_name]
    return tensor

