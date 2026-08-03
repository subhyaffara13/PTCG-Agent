import re

def parse_py(s, **kwargs):
    """Parse a string into a (nbformat, string) tuple."""
    nbf = current_nbformat
    nbm = current_nbformat_minor

    pattern = r"# <nbformat>(?P<nbformat>\d+[\.\d+]*)</nbformat>"
    m = re.search(pattern, s)
    if m is not None:
        digits = m.group("nbformat").split(".")
        nbf = int(digits[0])
        if len(digits) > 1:
            nbm = int(digits[1])

    return nbf, nbm, s

