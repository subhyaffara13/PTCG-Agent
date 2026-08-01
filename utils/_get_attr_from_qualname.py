
def _get_attr_from_qualname(mod: torch.nn.Module, qualname: str) -> Any:
    attr_val = mod
    for atom in qualname.split("."):  # type: ignore[union-attr]
        if not hasattr(attr_val, atom):
            raise AttributeError(f"Node target {qualname} not found!")
        attr_val = getattr(attr_val, atom)
    return attr_val

