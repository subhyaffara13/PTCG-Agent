
def format_float_positional(x, precision=None, unique=True,
                            fractional=True, trim='k', sign=False,
                            pad_left=None, pad_right=None, min_digits=None):
    """
    Format a floating-point scalar as a decimal string in positional notation.

    Provides control over rounding, trimming and padding. Uses and assumes
    IEEE unbiased rounding. Uses the "Dragon4" algorithm.

    Parameters
    ----------
    x : python float or numpy floating scalar
        Value to format.
    precision : non-negative integer or None, optional
        Maximum number of digits to print. May be None if `unique` is
        `True`, but must be an integer if unique is `False`.
    unique : boolean, optional
        If `True`, use a digit-generation strategy which gives the shortest
        representation which uniquely identifies the floating-point number from
        other values of the same type, by judicious rounding. If `precision`
        is given fewer digits than necessary can be printed, or if `min_digits`
        is given more can be printed, in which cases the last digit is rounded
        with unbiased rounding.
        If `False`, digits are generated as if printing an infinite-precision
        value and stopping after `precision` digits, rounding the remaining
        value with unbiased rounding
    fractional : boolean, optional
        If `True`, the cutoffs of `precision` and `min_digits` refer to the
        total number of digits after the decimal point, including leading
        zeros.
        If `False`, `precision` and `min_digits` refer to the total number of
        significant digits, before or after the decimal point, ignoring leading
        zeros.
    trim : one of 'k', '.', '0', '-', optional
        Controls post-processing trimming of trailing digits, as follows:

        * 'k' : keep trailing zeros, keep decimal point (no trimming)
        * '.' : trim all trailing zeros, leave decimal point
        * '0' : trim all but the zero before the decimal point. Insert the
          zero if it is missing.
        * '-' : trim trailing zeros and any trailing decimal point
    sign : boolean, optional
        Whether to show the sign for positive values.
    pad_left : non-negative integer, optional
        Pad the left side of the string with whitespace until at least that
        many characters are to the left of the decimal point.
    pad_right : non-negative integer, optional
        Pad the right side of the string with whitespace until at least that
        many characters are to the right of the decimal point.
    min_digits : non-negative integer or None, optional
        Minimum number of digits to print. Only has an effect if `unique=True`
        in which case additional digits past those necessary to uniquely
        identify the value may be printed, rounding the last additional digit.

        .. versionadded:: 1.21.0

    Returns
    -------
    rep : string
        The string representation of the floating point value

    See Also
    --------
    format_float_scientific

    Examples
    --------
    >>> import numpy as np
    >>> np.format_float_positional(np.float32(np.pi))
    '3.1415927'
    >>> np.format_float_positional(np.float16(np.pi))
    '3.14'
    >>> np.format_float_positional(np.float16(0.3))
    '0.3'
    >>> np.format_float_positional(np.float16(0.3), unique=False, precision=10)
    '0.3000488281'
    """
    precision = _none_or_positive_arg(precision, 'precision')
    pad_left = _none_or_positive_arg(pad_left, 'pad_left')
    pad_right = _none_or_positive_arg(pad_right, 'pad_right')
    min_digits = _none_or_positive_arg(min_digits, 'min_digits')
    if not fractional and precision == 0:
        raise ValueError("precision must be greater than 0 if "
                         "fractional=False")
    if min_digits > 0 and precision > 0 and min_digits > precision:
        raise ValueError("min_digits must be less than or equal to precision")
    return dragon4_positional(x, precision=precision, unique=unique,
                              fractional=fractional, trim=trim,
                              sign=sign, pad_left=pad_left,
                              pad_right=pad_right, min_digits=min_digits)

