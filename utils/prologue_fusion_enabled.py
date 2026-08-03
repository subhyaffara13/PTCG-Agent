import os

def prologue_fusion_enabled() -> bool:
    ENABLE_PROLOGUE_FUSION_VERSION = 0

    if "TORCHINDUCTOR_PROLOGUE_FUSION" in os.environ:
        return os.environ.get("TORCHINDUCTOR_PROLOGUE_FUSION") == "1"
    elif is_fbcode():
        jk_name = "pytorch/inductor:prologue_fusion_version"
        version = torch._utils_internal.justknobs_getval_int(jk_name)
        return version <= ENABLE_PROLOGUE_FUSION_VERSION
    else:
        return True

