
def get_legacy_mod_inlinelist() -> set[str]:
    torch_dir = _module_dir(torch)
    if torch_dir is None:
        return set()
    inlinelist = {
        _as_posix_path(torch_dir + m[len("torch.") :].replace(".", "/"))
        for m in LEGACY_MOD_INLINELIST
    }
    return inlinelist

