from typing import Any

def _compile_and_eval(
    script: str,
    globs: dict[str, Any] | None,
    locs: Mapping[str, object] | None = None,
    filename: str = "",
) -> None:
    """
    Evaluate the script with the given global (globs) and local (locs)
    variables.
    """
    bytecode = compile(script, filename, "exec")
    eval(bytecode, globs, locs)

