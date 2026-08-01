
def _remove_dups(L):
    """
    Remove duplicates AND preserve the original order of the elements.

    The set class is not guaranteed to do this.
    """
    seen_before = set()
    L2 = []
    for i in L:
        if i not in seen_before:
            seen_before.add(i)
            L2.append(i)
    return L2

