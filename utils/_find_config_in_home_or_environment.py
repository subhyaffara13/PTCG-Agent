import os
from pathlib import Path


def _find_config_in_home_or_environment() -> Iterator[Path]:
    """Find a config file in the specified environment var or the home directory."""
    if "PYLINTRC" in os.environ and Path(os.environ["PYLINTRC"]).exists():
        if Path(os.environ["PYLINTRC"]).is_file():
            yield Path(os.environ["PYLINTRC"]).resolve()
    else:
        try:
            user_home = Path.home()
        except RuntimeError:
            # If the home directory does not exist a RuntimeError will be raised
            user_home = None

        if user_home is not None and str(user_home) not in ("~", "/root"):
            home_rc = user_home / ".pylintrc"
            if home_rc.is_file():
                yield home_rc.resolve()

            home_rc = user_home / ".config" / "pylintrc"
            if home_rc.is_file():
                yield home_rc.resolve()

