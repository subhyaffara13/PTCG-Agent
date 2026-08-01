
def masked_select_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )
    inp = new_kwargs.pop("input")
    mask = new_kwargs.pop("mask")

    if inp.ndim > 2:
        raise RuntimeError("masked_select only support 2-D selections currently")
    elif inp.shape != mask.shape:
        raise RuntimeError(
            f"Mask with shape {mask.shape} is not compatible with input's shape {inp.shape}"
        )
    res_values = inp._values.masked_select(mask.values())
    mask_cumsum = F.pad(mask.values().cumsum(dim=0), (1, 0))  # type: ignore[arg-type]

    args = extract_kwargs(inp)
    args["offsets"] = mask_cumsum[inp._offsets]
    return NestedTensor(
        values=res_values,
        **args,
    )

