
def is_jumanpp_available() -> bool:
    return _is_package_available("rhoknp")[0] and shutil.which("jumanpp") is not None

