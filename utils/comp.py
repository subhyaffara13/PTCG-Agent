
def comp(z1, z2, tol=None):
    r"""Return a bool indicating whether the error between z1 and z2
    is $\le$ ``tol``.

    Examples
    ========

    If ``tol`` is ``None`` then ``True`` will be returned if
    :math:`|z1 - z2|\times 10^p \le 5` where $p$ is minimum value of the
    decimal precision of each value.

    >>> from sympy import comp, pi
    >>> pi4 = pi.n(4); pi4
    3.142
    >>> comp(_, 3.142)
    True
    >>> comp(pi4, 3.141)
    False
    >>> comp(pi4, 3.143)
    False

    A comparison of strings will be made
    if ``z1`` is a Number and ``z2`` is a string or ``tol`` is ''.

    >>> comp(pi4, 3.1415)
    True
    >>> comp(pi4, 3.1415, '')
    False

    When ``tol`` is provided and $z2$ is non-zero and
    :math:`|z1| > 1` the error is normalized by :math:`|z1|`:

    >>> abs(pi4 - 3.14)/pi4
    0.000509791731426756
    >>> comp(pi4, 3.14, .001)  # difference less than 0.1%
    True
    >>> comp(pi4, 3.14, .0005)  # difference less than 0.1%
    False

    When :math:`|z1| \le 1` the absolute error is used:

    >>> 1/pi4
    0.3183
    >>> abs(1/pi4 - 0.3183)/(1/pi4)
    3.07371499106316e-5
    >>> abs(1/pi4 - 0.3183)
    9.78393554684764e-6
    >>> comp(1/pi4, 0.3183, 1e-5)
    True

    To see if the absolute error between ``z1`` and ``z2`` is less
    than or equal to ``tol``, call this as ``comp(z1 - z2, 0, tol)``
    or ``comp(z1 - z2, tol=tol)``:

    >>> abs(pi4 - 3.14)
    0.00160156249999988
    >>> comp(pi4 - 3.14, 0, .002)
    True
    >>> comp(pi4 - 3.14, 0, .001)
    False
    """
    if isinstance(z2, str):
        if not pure_complex(z1, or_real=True):
            raise ValueError('when z2 is a str z1 must be a Number')
        return str(z1) == z2
    if not z1:
        z1, z2 = z2, z1
    if not z1:
        return True
    if not tol:
        a, b = z1, z2
        if tol == '':
            return str(a) == str(b)
        if tol is None:
            a, b = sympify(a), sympify(b)
            if not all(i.is_number for i in (a, b)):
                raise ValueError('expecting 2 numbers')
            fa = a.atoms(Float)
            fb = b.atoms(Float)
            if not fa and not fb:
                # no floats -- compare exactly
                return a == b
            # get a to be pure_complex
            for _ in range(2):
                ca = pure_complex(a, or_real=True)
                if not ca:
                    if fa:
                        a = a.n(prec_to_dps(min(i._prec for i in fa)))
                        ca = pure_complex(a, or_real=True)
                        break
                    else:
                        fa, fb = fb, fa
                        a, b = b, a
            cb = pure_complex(b)
            if not cb and fb:
                b = b.n(prec_to_dps(min(i._prec for i in fb)))
                cb = pure_complex(b, or_real=True)
            if ca and cb and (ca[1] or cb[1]):
                return all(comp(i, j) for i, j in zip(ca, cb))
            tol = 10**prec_to_dps(min(a._prec, getattr(b, '_prec', a._prec)))
            return int(abs(a - b)*tol) <= 5
    diff = abs(z1 - z2)
    az1 = abs(z1)
    if z2 and az1 > 1:
        return diff/az1 <= tol
    else:
        return diff <= tol

