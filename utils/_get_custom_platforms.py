
def _get_custom_platforms(arch: str) -> list[str]:
    arch_prefix, arch_sep, arch_suffix = arch.partition("_")
    if arch.startswith("macosx"):
        arches = _mac_platforms(arch)
    elif arch.startswith("ios"):
        arches = _ios_platforms(arch)
    elif arch_prefix == "android":
        arches = _android_platforms(arch)
    elif arch_prefix in ["manylinux2014", "manylinux2010"]:
        arches = _custom_manylinux_platforms(arch)
    else:
        arches = [arch]
    return arches

