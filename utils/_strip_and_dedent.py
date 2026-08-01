
def _strip_and_dedent(s):
    """For triple-quote strings"""
    return textwrap.dedent(s.lstrip("\n").rstrip())

