from pathlib import Path


def is_free_format(fname):
    """Check if file is in free format Fortran."""
    # f90 allows both fixed and free format, assuming fixed unless
    # signs of free format are detected.
    result = False
    if Path(fname).suffix.lower() in COMMON_FREE_EXTENSIONS:
        result = True
    with openhook(fname, 'r') as fhandle:
        line = fhandle.readline()
        n = 15  # the number of non-comment lines to scan for hints
        if _has_f_header(line):
            n = 0
        elif _has_f90_header(line):
            n = 0
            result = True
        while n > 0 and line:
            if line[0] != '!' and line.strip():
                n -= 1
                if (line[0] != '\t' and _free_f90_start(line[:5])) or line[-2:-1] == '&':
                    result = True
                    break
            line = fhandle.readline()
    return result

