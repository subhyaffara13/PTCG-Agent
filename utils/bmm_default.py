
def bmm_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    other = new_kwargs.pop("mat2")

    if inp.dim() != 3:
        raise ValueError("bmm(): input must be 3D")
    if other.dim() != 3:
        raise ValueError("bmm(): mat2 must be 3D")

    return matmul_default(torch.ops.aten.matmul.default, inp, other)

