import os
import sys
from typing import Any

def _typer_main_shell_completion(
    self: click.core.Command,
    *,
    ctx_args: MutableMapping[str, Any],
    prog_name: str,
    complete_var: str | None = None,
) -> None:
    if complete_var is None:
        complete_var = f"_{prog_name}_COMPLETE".replace("-", "_").upper()

    instruction = os.environ.get(complete_var)

    if not instruction:
        return

    from .completion import shell_complete

    rv = shell_complete(self, ctx_args, prog_name, complete_var, instruction)
    sys.exit(rv)

