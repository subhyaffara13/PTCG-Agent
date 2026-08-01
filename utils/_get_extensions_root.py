
def _get_extensions_root() -> Path:
    root_dir = EXTENSIONS_ROOT.expanduser()
    root_dir.mkdir(parents=True, exist_ok=True)
    return root_dir

