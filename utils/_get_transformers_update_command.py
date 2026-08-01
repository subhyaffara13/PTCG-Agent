
def _get_transformers_update_command() -> list[str] | None:
    """Return the command to update transformers as an argv list, or None if the installation method is unknown."""
    match installation_method():
        case "hf_installer" if os.name == "nt":
            return [
                "powershell",
                "-NoProfile",
                "-Command",
                "iwr -useb https://hf.co/cli/install.ps1 | iex -WithTransformers",
            ]
        case "hf_installer":
            return ["bash", "-c", "curl -LsSf https://hf.co/cli/install.sh | bash -s -- --with-transformers"]
        case "pip":
            return [sys.executable, "-m", "pip", "install", "-U", "transformers"]
        case _:
            return None

