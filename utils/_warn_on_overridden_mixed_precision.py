
def _warn_on_overridden_mixed_precision(
    overridden_module_classes: set[type[nn.Module]],
):
    if len(overridden_module_classes) == 0:
        return
    warnings.warn(
        "Both mixed precision and an auto_wrap_policy were specified to FSDP, "
        f"where the wrapped module has submodules of type:\n{overridden_module_classes}\n"
        "These modules will be wrapped as separate FSDP instacnes with mixed "
        "precision disabled.",
        stacklevel=2,
    )

