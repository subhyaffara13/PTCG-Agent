
def _dev_pkgs() -> set[str]:
    pkgs = {"pip"}

    if _should_suppress_build_backends():
        pkgs |= {"setuptools", "distribute", "wheel"}

    return pkgs

