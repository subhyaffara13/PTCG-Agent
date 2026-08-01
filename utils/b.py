
def b(x): # deal with b'foo' versus 'foo'
    import codecs
    return codecs.latin_1_encode(x)[0]


def b(s):
    # Useful for very coarse version differentiation.
    PY2 = sys.version_info[0] == 2
    PY3 = sys.version_info[0] == 3
    if PY3:
        return s.encode("utf-8")
    else:
        return s


def B(x, k, i, t):
    if k == 0:
        return 1.0 if t[i] <= x < t[i+1] else 0.0
    if t[i+k] == t[i]:
        c1 = 0.0
    else:
        c1 = (x - t[i])/(t[i+k] - t[i]) * B(x, k-1, i, t)
    if t[i+k+1] == t[i+1]:
        c2 = 0.0
    else:
        c2 = (t[i+k+1] - x)/(t[i+k+1] - t[i+1]) * B(x, k-1, i+1, t)
    return c1 + c2


def b(df, cols):
    return df.drop_duplicates(subset=cols[:-1])

