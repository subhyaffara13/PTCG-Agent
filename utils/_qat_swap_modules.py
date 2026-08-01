
def _qat_swap_modules(
    root: torch.nn.Module, module_to_qat_module: dict[Pattern, type[torch.nn.Module]]
) -> None:
    convert(root, mapping=module_to_qat_module, inplace=True, remove_qconfig=False)

