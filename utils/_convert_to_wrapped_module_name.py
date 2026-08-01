
def _convert_to_wrapped_module_name(module_name: str) -> str:
    module_name = module_name.replace(f"{FSDP_PREFIX}", "")
    module_name = module_name.replace(f"{FSDP_WRAPPED_MODULE}", "")
    if module_name:
        module_name = f"{module_name}."
    # `CheckpointWrapper` adds a prefix that has to be removed as well.
    module_name = module_name.replace(checkpoint_wrapper._CHECKPOINT_PREFIX, "")
    return module_name

