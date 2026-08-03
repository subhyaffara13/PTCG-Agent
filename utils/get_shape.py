from typing import Any

def get_shape(x: Any) -> TensorShapeType:
    """Get the shape of the array-like object `x`. If `x` is not array-like, raise an error.

    Array-like objects are those that have a `shape` attribute, are sequences of BaseTypes, or are BaseTypes.
    BaseTypes are defined as `bool`, `int`, `float`, `complex`, `str`, and `bytes`.
    """
    if hasattr(x, "shape"):
        return x.shape
    elif isinstance(x, _BaseTypes):
        return ()
    elif isinstance(x, Sequence):
        shape = []
        while isinstance(x, Sequence) and not isinstance(x, _BaseTypes):
            shape.append(len(x))
            x = x[0]
        return tuple(shape)
    else:
        raise ValueError(f"Cannot determine the shape of {x}, can only determine the shape of array-like objects.")


def get_shape(i):
    if isinstance(i, torch.Tensor):
        return i.shape
    return i


def get_shape(expr):
    if hasattr(expr, "shape"):
        return expr.shape
    return ()

