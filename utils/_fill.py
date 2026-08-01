
def _fill(strings, linelen=75):
    """
    Make one string from sequence of strings, with whitespace in between.

    The whitespace is chosen to form lines of at most *linelen* characters,
    if possible.
    """
    currpos = 0
    lasti = 0
    result = []
    for i, s in enumerate(strings):
        length = len(s)
        if currpos + length < linelen:
            currpos += length + 1
        else:
            result.append(b' '.join(strings[lasti:i]))
            lasti = i
            currpos = length
    result.append(b' '.join(strings[lasti:]))
    return b'\n'.join(result)

