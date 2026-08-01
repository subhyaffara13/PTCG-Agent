
def get_architecture() -> Arch:
    try:
        machine = platform.machine().lower()
    except Exception:
        return "unknown"

    if machine in ("arm64", "aarch64"):
        return "arm64"

    # TODO: untested
    if machine == "arm":
        return "arm"

    if machine == "x86_64":
        return "x64"

    # TODO: untested
    if sys.maxsize <= 2**32:
        return "x32"

    if machine:
        return OtherArch(machine)

    return "unknown"

