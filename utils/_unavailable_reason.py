
def _unavailable_reason(deps: list[tuple[str, str]]) -> None | str:
    """
    Check availability of required packages - cuteDSL & deps,
    informing user what (if anything) is missing

    NOTE: Doesn't actually import anything.
    """
    for package_name, module_name in deps:
        # Note this doesn't actually import the packages
        if importlib.util.find_spec(module_name) is None:
            return (
                f"missing optional dependency `{package_name}` "
                f"(importlib.util.find_spec({package_name}) failed)"
            )
    return None

