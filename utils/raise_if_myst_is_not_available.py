
def raise_if_myst_is_not_available():
    if not is_myst_available():
        raise ImportError("The MyST Markdown format requires python >= 3.6 and markdown-it-py~=1.0")

