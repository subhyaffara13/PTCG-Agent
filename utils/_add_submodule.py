
def _add_submodule(
    mod: torch.nn.Module,
    target: str,
    module_to_add: torch.nn.Module,
    create_module: Callable[[str], torch.nn.Module] | None = None,
):
    *prefix, field = target.split(".")

    for i, item in enumerate(prefix):
        submod = getattr(mod, item, None)

        if submod is None:
            if create_module is not None:
                submod = create_module(".".join(prefix[: i + 1]))
            else:
                submod = torch.nn.Module()
            setattr(mod, item, submod)

        if not isinstance(submod, torch.nn.Module):
            return False

        mod = submod

    mod.add_module(field, module_to_add)

