
def format_flags(flags):
    names = []
    for flag, name in [
        (PAI_CONTIGUOUS, "CONTIGUOUS"),
        (PAI_FORTRAN, "FORTRAN"),
        (PAI_ALIGNED, "ALIGNED"),
        (PAI_NOTSWAPPED, "NOTSWAPPED"),
        (PAI_WRITEABLE, "WRITEABLE"),
        (PAI_ARR_HAS_DESCR, "ARR_HAS_DESCR"),
    ]:
        if flag & flags:
            names.append(name)
    return ", ".join(names)

