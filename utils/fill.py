
def fill(*args, data: DataParamType = None, **kwargs) -> list[Polygon]:
    return gca().fill(*args, **({"data": data} if data is not None else {}), **kwargs)


def fill(a: TensorLikeType, value: NumberType) -> TensorLikeType:
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")
    if not isinstance(value, Number):
        raise AssertionError(f"value must be Number, got {type(value)}")

    python_type = utils.dtype_to_type(a.dtype)
    if not utils.is_weakly_lesser_type(type(value), python_type):
        msg = f"value argument of type {type(value)} cannot be safely cast to type {python_type}!"
        raise ValueError(msg)

    return prims.fill(a, value)


def fill(g: jit_utils.GraphContext, self, value):
    scalar_type = _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.FLOAT
    )
    return full_like(g, self, value, scalar_type)

