
def _call_name(base: str, n: int) -> str:
    # Given n >= 0, generate call names to a submodule `base` of the form
    # `base`, `base@1`, `base@2`, etc.
    return base if n == 1 else f"{base}@{n - 1}"

