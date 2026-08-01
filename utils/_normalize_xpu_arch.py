
def _normalize_xpu_arch(arch: str) -> str:
    if arch.startswith("Xe"):
        return arch[2:]
    if 12 <= int(arch) and int(arch) <= 50:
        return arch
    else:
        raise NotImplementedError(f"Unsupported xpu arch: {arch}")

