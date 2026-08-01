
def _shared_param_name_infos(
    module: nn.Module, fsdp_state
) -> Iterator[tuple[str, str, str]]:
    for param_name, module_name in _module_handle(
        fsdp_state, module
    ).shared_param_module_names():
        module_name = _convert_to_wrapped_module_name(module_name)
        fqn = f"{module_name}{param_name}"
        yield fqn, param_name, module_name

