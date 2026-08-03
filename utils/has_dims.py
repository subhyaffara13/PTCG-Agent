from typing import Any

def has_dims(obj: Any) -> bool:
    """
    Check if an object has first-class dimensions.

    This function checks if the object is either a Dim or a functorch Tensor
    that has first-class dimensions, using the proper check_exact methods.
    """
    from . import Dim, Tensor

    return Dim.check_exact(obj) or Tensor.check_exact(obj)

