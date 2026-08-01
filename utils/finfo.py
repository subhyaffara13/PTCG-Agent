
def finfo(dtyp):
    torch_dtype = _dtypes.dtype(dtyp).torch_dtype
    return torch.finfo(torch_dtype)


def finfo(type_: DType | Array, /, xp: Namespace) -> Any:
    # It is surprisingly difficult to recognize a dtype apart from an array.
    # np.int64 is not the same as np.asarray(1).dtype!
    try:
        return xp.finfo(type_)
    except (ValueError, TypeError):
        return xp.finfo(type_.dtype)

