
def _split_and_sort(s):
    """For output which does not require specific line order"""
    return sorted(_strip_and_dedent(s).splitlines())

