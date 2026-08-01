
def compute_symint_placeholders(lst: Iterable[None | int | SymInt]) -> list[bool]:
    # Non-nested symints are replaced with None in `make_runtime_safe()`
    return [s is None for s in lst]

