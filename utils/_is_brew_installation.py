import sys
from pathlib import Path


def _is_brew_installation() -> bool:
    """Check if running from a Homebrew installation.

    Homebrew installs the `hf` formula into a Cellar directory and creates a
    libexec virtualenv at e.g. /opt/homebrew/Cellar/hf/0.30.0/libexec/.
    We check `sys.prefix` (the venv/prefix root) for "/Cellar/hf/" rather
    than checking `sys.executable` — the latter resolves to Homebrew's Python
    (e.g. /opt/homebrew/Cellar/python@3.12/...) even for non-brew installs
    when the system Python happens to come from Homebrew.
    """
    prefix = str(Path(sys.prefix).resolve())
    return "/Cellar/hf/" in prefix

