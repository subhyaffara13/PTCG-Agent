
def _compile_firstset(info, fs):
    "Compiles the firstset for the pattern."
    reverse = bool(info.flags & REVERSE)
    fs = _check_firstset(info, reverse, fs)
    if not fs or isinstance(fs, AnyAll):
        return []

    # Compile the firstset.
    return fs.compile(reverse)

