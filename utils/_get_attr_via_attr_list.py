
def _get_attr_via_attr_list(model: torch.nn.Module, attr_list: list[str]):
    if len(attr_list) == 0:
        return model
    *prefix, field = attr_list
    t = model
    for item in prefix:
        t = getattr(t, item, None)  # type: ignore[assignment]
        if t is None:
            raise AssertionError(f"Attribute '{item}' not found in model")

    return getattr(t, field)

