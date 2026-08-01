
def _compat_module_name() -> str:
    assert __name__.endswith(".common._helpers")
    return __name__.removesuffix(".common._helpers")

