
def _get_submodule(mod: torch.nn.Module, target: str):
    *prefix, field = target.split(".")

    for item in prefix:
        submod = getattr(mod, item, None)

        if submod is None:
            return None

        if not isinstance(submod, torch.nn.Module):
            return None

        mod = submod

    return getattr(mod, field, None)

