
def is_complex(t: Type) -> bool:
    t = get_proper_type(t)
    return is_generic(t) or isinstance(t, (FunctionLike, TupleType, TypeVarType))


def is_complex(input: TensorLikeType):
    return utils.is_complex_dtype(input.dtype)


def is_complex(x: Any, /) -> bool:
    """Utility to detect if a given object is (known) to be complex."""
    return (isinstance(x, Tensor) and _is_complex(x)) or isinstance(x, complex)


def is_complex(x: Array, xp: ModuleType) -> bool:
    return xp.isdtype(x.dtype, 'complex floating')

