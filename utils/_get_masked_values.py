from typing import Any, Optional

def _get_masked_values(
    sensitive_object: dict,
    ignore_sensitive_values: bool = False,
    mask_all_values: bool = False,
    unmasked_length: int = 4,
    number_of_asterisks: Optional[int] = 4,
    _depth: int = 0,
    _max_depth: int = 20,
) -> dict:
    """
    Internal debugging helper function

    Masks the headers of the request sent from LiteLLM

    Args:
        masked_length: Optional length for the masked portion (number of *). If set, will use exactly this many *
                     regardless of original string length. The total length will be unmasked_length + masked_length.
    """
    sensitive_keywords = [
        "authorization",
        "token",
        "key",
        "secret",
        "vertex_credentials",
        "credentials",
        "password",
        "passwd",
    ]

    def _mask_value(v: Any) -> Any:
        if isinstance(v, dict):
            if _depth >= _max_depth:
                return v
            return _get_masked_values(
                v,
                ignore_sensitive_values=ignore_sensitive_values,
                mask_all_values=mask_all_values,
                unmasked_length=unmasked_length,
                number_of_asterisks=number_of_asterisks,
                _depth=_depth + 1,
                _max_depth=_max_depth,
            )
        if not isinstance(v, str):
            return v
        if len(v) <= unmasked_length:
            return "*****"
        if number_of_asterisks is not None:
            return (
                v[: unmasked_length // 2]
                + "*" * number_of_asterisks
                + v[-unmasked_length // 2 :]
            )
        return (
            v[: unmasked_length // 2]
            + "*" * (len(v) - unmasked_length)
            + v[-unmasked_length // 2 :]
        )

    return {
        k: (
            v
            if ignore_sensitive_values
            or not any(
                sensitive_keyword in k.lower()
                for sensitive_keyword in sensitive_keywords
            )
            else _mask_value(v)
        )
        for k, v in sensitive_object.items()
    }

