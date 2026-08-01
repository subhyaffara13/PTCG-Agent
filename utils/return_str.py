
def return_str(rets: tuple[Return, ...], names: list[str]) -> str:
    if len(rets) != len(names):
        raise AssertionError(f"Expected {len(rets)} names, got {len(names)}")
    if len(rets) == 0:
        return ""
    elif len(rets) == 1:
        return f"return {names[0]};"
    else:
        return f"return {dispatcher.returns_type(rets).cpp_type()}({', '.join(names)});"


def return_str(rets: tuple[Return, ...], names: list[str]) -> str:
    if len(rets) != len(names):
        raise AssertionError(
            f"Returns and names length mismatch: {len(rets)} vs {len(names)}"
        )
    if len(rets) == 0:
        return ""
    elif len(rets) == 1:
        return f"return {names[0]};"
    else:
        return f"return {dispatcher.returns_type(rets).cpp_type()}({', '.join(names)});"

