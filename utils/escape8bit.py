
def escape8bit(data):
    """Input is Unicode string."""

    def escapechar(c):
        n = ord(c)
        if 32 <= n <= 127 and c not in "<&>":
            return c
        else:
            return "&#" + repr(n) + ";"

    return strjoin(map(escapechar, data.decode("latin-1")))

