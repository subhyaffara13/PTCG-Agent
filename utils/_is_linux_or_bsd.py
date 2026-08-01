
def _is_linux_or_bsd() -> bool:
    if platform.system() == "Linux":
        return True

    return "BSD" in platform.system()

