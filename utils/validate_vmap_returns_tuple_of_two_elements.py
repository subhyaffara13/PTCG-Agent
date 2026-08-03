from typing import Any

def validate_vmap_returns_tuple_of_two_elements(result: Any) -> None:
    base_error_msg = (
        "Expected the vmap staticmethod to have two returns, an output "
        "and out_dims with pytree structure compatible with the output. "
    )
    if not isinstance(result, tuple):
        raise RuntimeError(base_error_msg + f"Got a {type(result)} instead")
    if not len(result) == 2:
        raise RuntimeError(base_error_msg + f"Got {len(result)} returns instead")

