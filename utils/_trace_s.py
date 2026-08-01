
def _trace_S(s, j, b, S_cosets):
    """
    Return the representative h satisfying s[h[b]] == j

    If there is not such a representative return None
    """
    for h in S_cosets[b]:
        if s[h[b]] == j:
            return h
    return None

