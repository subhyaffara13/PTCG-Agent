
def _clone_cutlass_paths(build_root: str) -> list[str]:
    paths = _cutlass_paths()
    cutlass_root = _cutlass_path()
    for path in _cutlass_paths():
        old_path = os.path.join(cutlass_root, path)
        new_path = os.path.join(build_root, path)
        shutil.copytree(old_path, new_path, dirs_exist_ok=True)
    return paths

