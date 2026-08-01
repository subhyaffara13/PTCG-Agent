
def _run_mixed_precision_override_policy(
    root_module: nn.Module,
    module_classes: Iterable[type[nn.Module]],
    ignored_modules: set[nn.Module],
    root_kwargs: dict[str, Any],
    target_module_to_kwargs: dict[nn.Module, dict[str, Any]],
):
    module_classes_tuple = tuple(set(module_classes))
    for module in root_module.modules():
        if module in ignored_modules:
            continue
        elif isinstance(module, module_classes_tuple):
            # This policy overrides any existing policy
            if module not in target_module_to_kwargs:
                # Only inherit from the root kwargs if not already specified
                target_module_to_kwargs[module] = root_kwargs
            target_module_to_kwargs[module]["mixed_precision"] = None
    return target_module_to_kwargs

