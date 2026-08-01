
def pandoc_version():
    """Pandoc's version number"""
    try:
        return pandoc("--version").splitlines()[0].split()[1]
    except OSError:
        return "N/A"

