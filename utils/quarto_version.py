
def quarto_version():
    """Quarto's version number"""
    try:
        return quarto("--version").strip()
    except OSError:
        return "N/A"

