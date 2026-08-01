
def unreplace_parenthesis(s, d):
    """Inverse of replace_parenthesis.
    """
    for k, v in d.items():
        p = _get_parenthesis_kind(k)
        left = {'ROUND': '(', 'SQUARE': '[', 'CURLY': '{', 'ROUNDDIV': '(/'}[p]
        right = {'ROUND': ')', 'SQUARE': ']', 'CURLY': '}', 'ROUNDDIV': '/)'}[p]
        s = s.replace(k, left + v + right)
    return s

