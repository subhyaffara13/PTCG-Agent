from typing import Any

def _check_custom_op_aliasing(
    name: str, args: tuple[Any, ...], kwargs: dict[str, Any], result: Any
) -> None:
    """
    Check if custom op outputs alias inputs or other outputs.
    If config.error_on_custom_op_aliasing is True, raises RuntimeError.
    Otherwise, emits a warning.
    """
    try:
        torch._library.utils._c_check_aliasing_constraint(
            name,
            args,
            kwargs,
            result,
        )
    except RuntimeError as e:
        if config.error_on_custom_op_aliasing:
            raise
        else:
            msg = f"{e} This is deprecated and will become an error in PyTorch 2.12."
            warnings.warn(msg, UserWarning, stacklevel=3)

