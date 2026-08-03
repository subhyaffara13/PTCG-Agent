import sys
from typing import Any

def lazy_format_graph_code(
    name: str, gm: torch.fx.GraphModule, maybe_id: int | None = None, **kwargs: Any
) -> LazyString:
    """
    Returns a LazyString that formats the graph code.
    """

    def format_name() -> str:
        if maybe_id is not None:
            return f"{name} {maybe_id}"
        else:
            return name

    if "print_output" not in kwargs:
        kwargs["print_output"] = False

    if "colored" in kwargs:
        try:
            if not sys.stdout.isatty():
                kwargs["colored"] = False
        except AttributeError:
            kwargs["colored"] = False

    return LazyString(
        lambda: _format_graph_code(
            f"===== {format_name()} =====\n",
            gm.forward.__code__.co_filename,
            gm.print_readable(**kwargs),
        )
    )

