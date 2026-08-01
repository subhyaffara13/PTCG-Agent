
def _maybe_convert_scalar_types_to_dtypes(
    scalar_types: list[Any],
) -> list[torch.dtype | None]:
    """
    When a list of `torch.dtype`s is passed through the dispatcher as
    `ScalarType[]`, it is converted to a list of scalar type enum values. This
    function converts it back to a list of `torch.dtype`s.
    """
    # Order defined in https://github.com/pytorch/pytorch/blob/344defc9733a45fee8d0c4d3f5530f631e823196/c10/core/ScalarType.h
    _SCALAR_TYPE_TO_DTYPE = {
        0: torch.uint8,
        1: torch.int8,
        2: torch.short,
        3: torch.int,
        4: torch.int64,
        5: torch.half,
        6: torch.float,
        7: torch.double,
        8: torch.complex32,
        9: torch.complex64,
        10: torch.complex128,
        11: torch.bool,
        12: torch.qint8,
        13: torch.quint8,
        14: torch.qint32,
        15: torch.bfloat16,
        16: torch.float8_e5m2,
        17: torch.float8_e4m3fn,
        18: torch.float8_e5m2fnuz,
        19: torch.float8_e4m3fnuz,
    }
    if any(not isinstance(x, (type(None), int)) for x in scalar_types):
        return scalar_types

    dtypes: list[torch.dtype | None] = []
    for scalar_type in scalar_types:
        if scalar_type is None:
            dtypes.append(scalar_type)
        elif scalar_type not in _SCALAR_TYPE_TO_DTYPE:
            raise ValueError(f"Unrecognized scalar type {scalar_type}")
        else:
            dtypes.append(_SCALAR_TYPE_TO_DTYPE[scalar_type])
    return dtypes

