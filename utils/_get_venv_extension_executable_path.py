
def _get_venv_extension_executable_path(venv_dir: Path, short_name: str) -> Path:
    executable_name = _get_executable_name(short_name)
    if os.name == "nt":
        return venv_dir / "Scripts" / executable_name
    return venv_dir / "bin" / executable_name

