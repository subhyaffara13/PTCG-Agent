
def get_mod_skiplist() -> set[str]:
    torch_dir = _module_dir(torch)
    if torch_dir is None:
        return set()
    skiplist = {
        _as_posix_path(torch_dir + m[len("torch.") :].replace(".", "/"))
        for m in MOD_SKIPLIST
    }
    return skiplist

