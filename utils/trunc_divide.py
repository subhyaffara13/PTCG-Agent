
def trunc_divide(a: TensorLikeType | NumberType, b: TensorLikeType | NumberType):
    dtype = utils.get_dtype(a)
    if utils.is_integer_dtype(dtype):
        return prims.div(a, b)

    return trunc(prims.div(a, b))

