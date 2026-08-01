
def get_xpu_arch() -> str | None:
    from torch.testing._internal.common_xpu import get_xpu_codename, XPUCodename

    name2arch = {
        XPUCodename.PVC: "Xe12",
        XPUCodename.BMG: "Xe20",
    }

    codename = get_xpu_codename()
    if not codename or codename not in name2arch:
        log.warning("Unknown XPU codename, cannot determine architecture")
        return None

    return name2arch[codename]


def get_xpu_arch() -> XPUArch | None:
    codename = get_xpu_codename()
    return _CODENAME_TO_ARCH.get(codename, XPUArch.Unknown)

