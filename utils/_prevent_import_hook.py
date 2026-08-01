
def _prevent_import_hook(name: str, args: tuple[Any, ...]) -> None:
    if name != "import":
        return
    module = args[0]
    if module in _MISSING_MODULES:
        raise ImportError(f"No module named {module!r}")
    if module.partition(".")[0] in _STDLIB_MODULE_NAMES:
        return
    deprecated(
        reason=f"Unexpected import of {module!r} after pip install started.",
        replacement=None,
        gone_in="26.3",
        issue=13842,
        include_source=True,
        stacklevel=3,
    )

