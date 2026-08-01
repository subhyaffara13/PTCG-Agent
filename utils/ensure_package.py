
def ensure_package(dir_path: Path):
    dir_path.mkdir(parents=True, exist_ok=True)
    init_file = dir_path / '__init__.py'
    if not init_file.exists():
        init_file.touch()

