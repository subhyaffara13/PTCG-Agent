
def sym_is_contiguous_general(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )
    inp = new_kwargs.pop("input")

    # If created from narrow() check for lengths
    if inp.lengths() is not None:
        return False

    new_kwargs["memory_format"] = new_kwargs.get(
        "memory_format", torch.contiguous_format
    )

    if new_kwargs["memory_format"] == torch.preserve_format:
        return True

    return torch.ops.aten.sym_is_contiguous.default(inp._values, **new_kwargs)

