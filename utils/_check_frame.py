
def _check_frame(other):
    from .vector import VectorTypeError
    if not isinstance(other, ReferenceFrame):
        raise VectorTypeError(other, ReferenceFrame('A'))

