import os

def get_default_options() -> list[str]:
    """Read config file and return list of options."""
    options = []
    home = os.environ.get("HOME", "")
    if home:
        rcfile = os.path.join(home, RCFILE)
        try:
            with open(rcfile, encoding="utf-8") as file_handle:
                options = file_handle.read().split()
        except OSError:
            pass  # ignore if no config file found
    return options

