
def center_pad(wstring, wtarget, fillchar=' '):
    """
    Return the padding strings necessary to center a string of
    wstring characters wide in a wtarget wide space.

    The line_width wstring should always be less or equal to wtarget
    or else a ValueError will be raised.
    """
    if wstring > wtarget:
        raise ValueError('not enough space for string')
    wdelta = wtarget - wstring

    wleft = wdelta // 2  # favor left '1 '
    wright = wdelta - wleft

    left = fillchar * wleft
    right = fillchar * wright

    return left, right

