import re

def _parse_size_hints(kernel_module_code: str, kernel_category: str) -> str | None:
    if kernel_category == "foreach":
        # foreach kernel does not have size_hints
        return None
    m = re.search(r"size_hints=(\[[0-9, ]*\]),", kernel_module_code)
    assert m, "size_hints missing!"
    return m.group(1)

