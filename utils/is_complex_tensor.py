from typing import Any

def is_complex_tensor(obj: Any, /) -> TypeIs[ComplexTensor]:
    r"""Returns True if the input is a ComplexTensor, else False

    Args:
        a: any input

    Examples:

        >>> # xdoctest: +SKIP
        >>> from torch.complex import ComplexTensor
        >>> data = torch.zeros((3, 2), dtype=torch.complex64)
        >>> ct = ComplexTensor.from_interleaved(data)
        >>> is_complex_tensor(ct)
        True
    """
    return isinstance(obj, ComplexTensor)

