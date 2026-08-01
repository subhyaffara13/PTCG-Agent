
def expand_to_tensor_dim(t, n):
    """
    Expand a type to the desired tensor dimension if possible
    Raise an error otherwise.
    - t is the given type
    - n is a number of dimensions to expand to
    """
    if t == Dyn:
        dims = [Dyn] * n
        return TensorType(tuple(dims))
    elif isinstance(t, TensorType):
        if len(t.__args__) != n:
            raise TypeError(
                f"Cannot extend tensor. Tensor {t} has rank {len(t.__args__)}. It should have rank {n}"
            )
        return t
    else:
        raise TypeError(f"Cannot match the type {t}")

