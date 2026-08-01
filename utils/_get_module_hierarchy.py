
def _get_module_hierarchy(mod: torch.nn.Module) -> dict[str, str]:
    return {
        name: type(m).__name__ for name, m in mod.named_modules(remove_duplicate=False)
    }

