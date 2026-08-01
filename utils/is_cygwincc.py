
def is_cygwincc(cc):
    """Try to determine if the compiler that would be used is from cygwin."""
    out_string = check_output(shlex.split(cc) + ['-dumpmachine'])
    return out_string.strip().endswith(b'cygwin')

