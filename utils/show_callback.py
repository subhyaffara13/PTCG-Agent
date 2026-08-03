import os
import sys
from typing import Any

def show_callback(ctx: click.Context, param: click.Parameter, value: Any) -> Any:
    if not value or ctx.resilient_parsing:
        return value  # pragma: no cover
    prog_name = ctx.find_root().info_name
    assert prog_name
    complete_var = "_{}_COMPLETE".format(prog_name.replace("-", "_").upper())
    shell = ""
    test_disable_detection = os.getenv("_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION")
    if isinstance(value, str):
        shell = value
    elif not test_disable_detection:
        detected_shell = _get_shell_name()
        if detected_shell is not None:
            shell = detected_shell
    script_content = get_completion_script(
        prog_name=prog_name, complete_var=complete_var, shell=shell
    )
    click.echo(script_content)
    sys.exit(0)

