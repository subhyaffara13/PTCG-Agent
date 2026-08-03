from typing import Any

def list_options() -> list[str]:
    r"""Returns a dictionary describing the optimizations and debug configurations
    that are available to `torch.compile()`.

    The options are documented in `torch._inductor.config`.

    Example::

        >>> torch._inductor.list_options()
    """

    from torch._inductor import config

    current_config: dict[str, Any] = config.get_config_copy()

    return list(current_config.keys())

