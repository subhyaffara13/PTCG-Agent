
def isRocmArchAnyOf(arch: tuple[str, ...]):
    if not torch.version.hip:
        return False
    rocmArch = getRocmArchName()
    return any(x in rocmArch for x in arch)

