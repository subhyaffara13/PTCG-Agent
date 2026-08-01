
def _get_musl_version(executable: str) -> _MuslVersion | None:
    """Detect currently-running musl runtime version.

    This is done by checking the specified executable's dynamic linking
    information, and invoking the loader to parse its output for a version
    string. If the loader is musl, the output would be something like::

        musl libc (x86_64)
        Version 1.2.2
        Dynamic Program Loader
    """
    try:
        with open(executable, "rb") as f:
            ld = ELFFile(f).interpreter
    except (OSError, TypeError, ValueError):
        return None
    if ld is None or "musl" not in ld:
        return None
    proc = subprocess.run([ld], check=False, stderr=subprocess.PIPE, text=True)
    return _parse_musl_version(proc.stderr)


def _get_musl_version(executable: str) -> _MuslVersion | None:
    """Detect currently-running musl runtime version.

    This is done by checking the specified executable's dynamic linking
    information, and invoking the loader to parse its output for a version
    string. If the loader is musl, the output would be something like::

        musl libc (x86_64)
        Version 1.2.2
        Dynamic Program Loader
    """
    try:
        with open(executable, "rb") as f:
            ld = ELFFile(f).interpreter
    except (OSError, TypeError, ValueError):
        return None
    if ld is None or "musl" not in ld:
        return None
    proc = subprocess.run([ld], check=False, stderr=subprocess.PIPE, text=True)
    return _parse_musl_version(proc.stderr)


def _get_musl_version(executable: str) -> Optional[_MuslVersion]:
    """Detect currently-running musl runtime version.

    This is done by checking the specified executable's dynamic linking
    information, and invoking the loader to parse its output for a version
    string. If the loader is musl, the output would be something like::

        musl libc (x86_64)
        Version 1.2.2
        Dynamic Program Loader
    """
    with contextlib.ExitStack() as stack:
        try:
            f = stack.enter_context(open(executable, "rb"))
        except IOError:
            return None
        ld = _parse_ld_musl_from_elf(f)
    if not ld:
        return None
    proc = subprocess.run([ld], stderr=subprocess.PIPE, universal_newlines=True)
    return _parse_musl_version(proc.stderr)


def _get_musl_version(executable: str) -> _MuslVersion | None:
    """Detect currently-running musl runtime version.

    This is done by checking the specified executable's dynamic linking
    information, and invoking the loader to parse its output for a version
    string. If the loader is musl, the output would be something like::

        musl libc (x86_64)
        Version 1.2.2
        Dynamic Program Loader
    """
    try:
        with open(executable, "rb") as f:
            ld = ELFFile(f).interpreter
    except (OSError, TypeError, ValueError):
        return None
    if ld is None or "musl" not in ld:
        return None
    proc = subprocess.run([ld], check=False, stderr=subprocess.PIPE, text=True)
    return _parse_musl_version(proc.stderr)

