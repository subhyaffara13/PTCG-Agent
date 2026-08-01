
def s_vars(n):
    """Form the symbols s1, s2, ..., sn to stand for elem. symm. polys. """
    return symbols([f's{i + 1}' for i in range(n)])

