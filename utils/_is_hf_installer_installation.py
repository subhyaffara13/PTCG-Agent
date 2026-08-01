
def _is_hf_installer_installation() -> bool:
    """Return `True` if the current environment was set up via the official hf installer script.

    i.e. using one of
        curl -LsSf https://hf.co/cli/install.sh | bash
        powershell -ExecutionPolicy ByPass -c "irm https://hf.co/cli/install.ps1 | iex"
    """
    venv = sys.prefix  # points to venv root if active
    marker = Path(venv) / ".hf_installer_marker"
    return marker.exists()

