from typing import Any

def title(
    label: str,
    fontdict: dict[str, Any] | None = None,
    loc: Literal["left", "center", "right"] | None = None,
    pad: float | None = None,
    *,
    y: float | None = None,
    **kwargs,
) -> Text:
    return gca().set_title(label, fontdict=fontdict, loc=loc, pad=pad, y=y, **kwargs)


def title(a):
    """
    Return element-wise title cased version of string or unicode.

    Title case words start with uppercase characters, all remaining cased
    characters are lowercase.

    Calls :meth:`str.title` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Input array.

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input types

    See Also
    --------
    str.title

    Examples
    --------
    >>> import numpy as np
    >>> c=np.array(['a1b c','1b ca','b ca1','ca1b'],'S5'); c
    array(['a1b c', '1b ca', 'b ca1', 'ca1b'],
        dtype='|S5')
    >>> np.strings.title(c)
    array(['A1B C', '1B Ca', 'B Ca1', 'Ca1B'],
        dtype='|S5')

    """
    a_arr = np.asarray(a)
    return _vec_string(a_arr, a_arr.dtype, 'title')

