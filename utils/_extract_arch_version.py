
def _extract_arch_version(arch_string: str) -> int:
    """Extracts the architecture string from a CUDA version"""
    base = arch_string.split("_", maxsplit=2)[1]
    base = base.removesuffix("a").removesuffix("f")
    return int(base)

