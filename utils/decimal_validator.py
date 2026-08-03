from typing import Any

def decimal_validator(v: Any) -> Decimal:
    if isinstance(v, Decimal):
        return v
    elif isinstance(v, (bytes, bytearray)):
        v = v.decode()

    v = str(v).strip()

    try:
        v = Decimal(v)
    except DecimalException:
        raise errors.DecimalError()

    if not v.is_finite():
        raise errors.DecimalIsNotFiniteError()

    return v

