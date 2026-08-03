import os
import sys

def _get_huggingface_hub_update_command() -> list[str] | None:
    """Return the command to update huggingface_hub as an argv list, or None if the installation method is unknown."""
    match installation_method():
        case "brew":
            return ["brew", "upgrade", "hf"]
        case "hf_installer" if os.name == "nt":
            return ["powershell", "-NoProfile", "-Command", "iwr -useb https://hf.co/cli/install.ps1 | iex"]
        case "hf_installer":
            return ["bash", "-c", "curl -LsSf https://hf.co/cli/install.sh | bash -"]
        case "pip":
            return [sys.executable, "-m", "pip", "install", "-U", "huggingface_hub"]
        case _:
            return None

