
def _parse_reduction_hint(kernel_category: str, kernel_module_code: str) -> str | None:
    if kernel_category not in ("reduction", "persistent_reduction"):
        return None
    m = re.search(r"reduction_hint=ReductionHint\.(\w*),", kernel_module_code)
    assert m, "reduction_hint not found in kernel source code!"
    return m.group(1)

