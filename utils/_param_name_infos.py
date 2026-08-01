
def _param_name_infos(
    module: nn.Module, fsdp_state: _FSDPState
) -> Iterator[tuple[str, str, str]]:
    if not _has_fsdp_params(fsdp_state, module):
        return
    for param_name, module_name in _module_handle(
        fsdp_state, module
    ).param_module_names():
        module_name = _convert_to_wrapped_module_name(module_name)
        fqn = f"{module_name}{param_name}"
        yield fqn, param_name, module_name

