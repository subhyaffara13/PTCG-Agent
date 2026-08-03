from typing import Any

def list_mode_options(
    mode: str | None = None, dynamic: bool | None = None
) -> dict[str, Any]:
    r"""Returns a dictionary describing the optimizations that each of the available
    modes passed to `torch.compile()` performs.

    Args:
        mode (str, optional): The mode to return the optimizations for.
        If None, returns optimizations for all modes
        dynamic (bool, optional): Whether dynamic shape is enabled.

    Example::
        >>> torch._inductor.list_mode_options()
    """

    mode_options: dict[str, dict[str, bool]] = {
        "default": {},
        # lite backend for opt-in optimizations
        "lite": lite_mode_options,
        # enable cudagraphs
        "reduce-overhead": {
            "triton.cudagraphs": True,
        },
        # enable max-autotune
        "max-autotune-no-cudagraphs": {
            "max_autotune": True,
            "coordinate_descent_tuning": True,
        },
        # enable max-autotune
        # enable cudagraphs
        "max-autotune": {
            "max_autotune": True,
            "triton.cudagraphs": True,
            "coordinate_descent_tuning": True,
        },
    }
    try:
        return mode_options[mode] if mode else mode_options
    except KeyError as e:
        raise RuntimeError(
            f"Unrecognized mode={mode}, should be one of: {', '.join(mode_options.keys())}"
        ) from e

