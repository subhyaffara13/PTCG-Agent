import sys

def _catch_valueerror(unraisable: sys.UnraisableHookArgs) -> None:  # pragma: no cover
    """Overwrite sys.unraisablehook to catch incorrect ValueError.

    Python 3.12 introduced changes that sometimes cause astroid to emit ValueErrors
    with 'generator already executing'. Fixed in Python 3.12.3 and 3.13.

    https://github.com/pylint-dev/pylint/issues/9138
    """
    if (
        isinstance(unraisable.exc_value, ValueError)
        and unraisable.exc_value.args[0] == "generator already executing"
    ):
        return

    sys.__unraisablehook__(unraisable)

