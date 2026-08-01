
def _has_attr(model: torch.nn.Module, attr_name: str):
    *prefix, field = attr_name.split(".")
    t = model
    for item in prefix:
        t = hasattr(t, item)  # type: ignore[assignment]
        if t is False:
            return False

    return hasattr(t, field)

