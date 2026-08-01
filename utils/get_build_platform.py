
def get_build_platform():
    """Return this platform's string for platform-specific distributions"""
    from sysconfig import get_platform

    plat = get_platform()
    if sys.platform == "darwin" and not plat.startswith('macosx-'):
        try:
            version = _macos_vers()
            machine = _macos_arch(os.uname()[4].replace(" ", "_"))
            return f"macosx-{version[0]}.{version[1]}-{machine}"
        except ValueError:
            # if someone is running a non-Mac darwin system, this will fall
            # through to the default implementation
            pass
    return plat

