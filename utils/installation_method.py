
def installation_method() -> Literal["brew", "hf_installer", "pip", "unknown"]:
    """Return the installation method of the current environment.

    - "hf_installer" if installed via the official installer script
    - "brew" if installed via Homebrew
    - "pip" if pip is available (default fallback for standard Python environments)
    - "unknown" otherwise
    """
    # hf_installer check must come first: the installer creates a venv using the
    # system Python, which may be Homebrew's. Checking brew first would false-positive
    # when the resolved sys.executable points to /opt/homebrew/... inside a venv.
    if _is_hf_installer_installation():
        return "hf_installer"
    if _is_brew_installation():
        return "brew"
    if _is_pip_available():
        return "pip"
    return "unknown"

