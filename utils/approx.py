
def approx(
    expected: Any,
    rel: float | Decimal | timedelta | None = None,
    abs: float | Decimal | timedelta | None = None,
    nan_ok: bool = False,
) -> ApproxBase:
    """Assert that two numbers (or two ordered sequences of numbers) are equal to each other
    within some tolerance.

    Due to the :doc:`python:tutorial/floatingpoint`, numbers that we
    would intuitively expect to be equal are not always so::

        >>> 0.1 + 0.2 == 0.3
        False

    This problem is commonly encountered when writing tests, e.g. when making
    sure that floating-point values are what you expect them to be.  One way to
    deal with this problem is to assert that two floating-point numbers are
    equal to within some appropriate tolerance::

        >>> abs((0.1 + 0.2) - 0.3) < 1e-6
        True

    However, comparisons like this are tedious to write and difficult to
    understand.  Furthermore, absolute comparisons like the one above are
    usually discouraged because there's no tolerance that works well for all
    situations.  ``1e-6`` is good for numbers around ``1``, but too small for
    very big numbers and too big for very small ones.  It's better to express
    the tolerance as a fraction of the expected value, but relative comparisons
    like that are even more difficult to write correctly and concisely.

    The ``approx`` class performs floating-point comparisons using a syntax
    that's as intuitive as possible::

        >>> from pytest import approx
        >>> 0.1 + 0.2 == approx(0.3)
        True

    The same syntax also works for ordered sequences of numbers::

        >>> (0.1 + 0.2, 0.2 + 0.4) == approx((0.3, 0.6))
        True

    ``numpy`` arrays::

        >>> import numpy as np                                                          # doctest: +SKIP
        >>> np.array([0.1, 0.2]) + np.array([0.2, 0.4]) == approx(np.array([0.3, 0.6])) # doctest: +SKIP
        True

    And for a ``numpy`` array against a scalar::

        >>> import numpy as np                                         # doctest: +SKIP
        >>> np.array([0.1, 0.2]) + np.array([0.2, 0.1]) == approx(0.3) # doctest: +SKIP
        True

    Only ordered sequences are supported, because ``approx`` needs
    to infer the relative position of the sequences without ambiguity. This means
    ``sets`` and other unordered sequences are not supported.

    Finally, dictionary *values* can also be compared::

        >>> {'a': 0.1 + 0.2, 'b': 0.2 + 0.4} == approx({'a': 0.3, 'b': 0.6})
        True

    The comparison will be true if both mappings have the same keys and their
    respective values match the expected tolerances.

    **Tolerances**

    By default, ``approx`` considers numbers within a relative tolerance of
    ``1e-6`` (i.e. one part in a million) of its expected value to be equal.
    This treatment would lead to surprising results if the expected value was
    ``0.0``, because nothing but ``0.0`` itself is relatively close to ``0.0``.
    To handle this case less surprisingly, ``approx`` also considers numbers
    within an absolute tolerance of ``1e-12`` of its expected value to be
    equal.  Infinity and NaN are special cases.  Infinity is only considered
    equal to itself, regardless of the relative tolerance.  NaN is not
    considered equal to anything by default, but you can make it be equal to
    itself by setting the ``nan_ok`` argument to True.  (This is meant to
    facilitate comparing arrays that use NaN to mean "no data".)

    Both the relative and absolute tolerances can be changed by passing
    arguments to the ``approx`` constructor::

        >>> 1.0001 == approx(1)
        False
        >>> 1.0001 == approx(1, rel=1e-3)
        True
        >>> 1.0001 == approx(1, abs=1e-3)
        True

    If you specify ``abs`` but not ``rel``, the comparison will not consider
    the relative tolerance at all.  In other words, two numbers that are within
    the default relative tolerance of ``1e-6`` will still be considered unequal
    if they exceed the specified absolute tolerance.  If you specify both
    ``abs`` and ``rel``, the numbers will be considered equal if either
    tolerance is met::

        >>> 1 + 1e-8 == approx(1)
        True
        >>> 1 + 1e-8 == approx(1, abs=1e-12)
        False
        >>> 1 + 1e-8 == approx(1, rel=1e-6, abs=1e-12)
        True

    **Non-numeric types**

    You can also use ``approx`` to compare non-numeric types, or dicts and
    sequences containing non-numeric types, in which case it falls back to
    strict equality. This can be useful for comparing dicts and sequences that
    can contain optional values::

        >>> {"required": 1.0000005, "optional": None} == approx({"required": 1, "optional": None})
        True
        >>> [None, 1.0000005] == approx([None,1])
        True
        >>> ["foo", 1.0000005] == approx([None,1])
        False

    **datetime and timedelta**

    You can also use ``approx`` to compare :class:`~datetime.datetime` and
    :class:`~datetime.timedelta` objects by specifying an absolute tolerance
    as a :class:`~datetime.timedelta`::

        >>> from datetime import datetime, timedelta
        >>> dt1 = datetime(2024, 1, 1, 12, 0, 0)
        >>> dt2 = datetime(2024, 1, 1, 12, 0, 0, 500000)
        >>> dt1 == approx(dt2, abs=timedelta(seconds=1))
        True

    Note that ``rel`` is not supported for datetime comparisons.
    For timedelta comparisons, ``rel`` is a number (not a timedelta) that
    represents a relative tolerance -- a fraction of the expected value.
    ``abs`` must be a ``timedelta`` object in both cases.

    .. versionadded:: 8.4

    If you're thinking about using ``approx``, then you might want to know how
    it compares to other good ways of comparing floating-point numbers.  All of
    these algorithms are based on relative and absolute tolerances and should
    agree for the most part, but they do have meaningful differences:

    - ``math.isclose(a, b, rel_tol=1e-9, abs_tol=0.0)``:  True if the relative
      tolerance is met w.r.t. either ``a`` or ``b`` or if the absolute
      tolerance is met.  Because the relative tolerance is calculated w.r.t.
      both ``a`` and ``b``, this test is symmetric (i.e.  neither ``a`` nor
      ``b`` is a "reference value").  You have to specify an absolute tolerance
      if you want to compare to ``0.0`` because there is no tolerance by
      default.  More information: :py:func:`math.isclose`.

    - ``numpy.isclose(a, b, rtol=1e-5, atol=1e-8)``: True if the difference
      between ``a`` and ``b`` is less that the sum of the relative tolerance
      w.r.t. ``b`` and the absolute tolerance.  Because the relative tolerance
      is only calculated w.r.t. ``b``, this test is asymmetric and you can
      think of ``b`` as the reference value.  Support for comparing sequences
      is provided by :py:func:`numpy.allclose`.  More information:
      :std:doc:`numpy:reference/generated/numpy.isclose`.

    - ``unittest.TestCase.assertAlmostEqual(a, b)``: True if ``a`` and ``b``
      are within an absolute tolerance of ``1e-7``.  No relative tolerance is
      considered , so this function is not appropriate for very large or very
      small numbers.  Also, it's only available in subclasses of ``unittest.TestCase``
      and it's ugly because it doesn't follow PEP8.  More information:
      :py:meth:`unittest.TestCase.assertAlmostEqual`.

    - ``a == pytest.approx(b, rel=1e-6, abs=1e-12)``: True if the relative
      tolerance is met w.r.t. ``b`` or if the absolute tolerance is met.
      Because the relative tolerance is only calculated w.r.t. ``b``, this test
      is asymmetric and you can think of ``b`` as the reference value.  In the
      special case that you explicitly specify an absolute tolerance but not a
      relative tolerance, only the absolute tolerance is considered.

    .. note::

        ``approx`` can handle numpy arrays, but we recommend the
        specialised test helpers in :std:doc:`numpy:reference/routines.testing`
        if you need support for comparisons, NaNs, or ULP-based tolerances.

        To match strings using regex, you can use
        `Matches <https://github.com/asottile/re-assert#re_assertmatchespattern-str-args-kwargs>`_
        from the
        `re_assert package <https://github.com/asottile/re-assert>`_.


    .. note::

        Unlike built-in equality, this function considers
        booleans unequal to numeric zero or one. For example::

           >>> 1 == approx(True)
           False

    .. warning::

       .. versionchanged:: 3.2

       In order to avoid inconsistent behavior, :py:exc:`TypeError` is
       raised for ``>``, ``>=``, ``<`` and ``<=`` comparisons.
       The example below illustrates the problem::

           assert approx(0.1) > 0.1 + 1e-10  # calls approx(0.1).__gt__(0.1 + 1e-10)
           assert 0.1 + 1e-10 > approx(0.1)  # calls approx(0.1).__lt__(0.1 + 1e-10)

       In the second example one expects ``approx(0.1).__le__(0.1 + 1e-10)``
       to be called. But instead, ``approx(0.1).__lt__(0.1 + 1e-10)`` is used to
       comparison. This is because the call hierarchy of rich comparisons
       follows a fixed behavior. More information: :py:meth:`object.__ge__`

    .. versionchanged:: 3.7.1
       ``approx`` raises ``TypeError`` when it encounters a dict value or
       sequence element of non-numeric type.

    .. versionchanged:: 6.1.0
       ``approx`` falls back to strict equality for non-numeric types instead
       of raising ``TypeError``.
    """
    # Delegate the comparison to a class that knows how to deal with the type
    # of the expected value (e.g. int, float, list, dict, numpy.array, etc).
    #
    # The primary responsibility of these classes is to implement ``__eq__()``
    # and ``__repr__()``.  The former is used to actually check if some
    # "actual" value is equivalent to the given expected value within the
    # allowed tolerance.  The latter is used to show the user the expected
    # value and tolerance, in the case that a test failed.
    #
    # The actual logic for making approximate comparisons can be found in
    # ApproxScalar, which is used to compare individual numbers.  All of the
    # other Approx classes eventually delegate to this class.  The ApproxBase
    # class provides some convenient methods and overloads, but isn't really
    # essential.

    __tracebackhide__ = True

    if isinstance(expected, Decimal):
        cls: type[ApproxBase] = ApproxDecimal
    elif isinstance(expected, Mapping):
        cls = ApproxMapping
    elif (np_array := _as_numpy_array(expected)) is not None:
        expected = np_array
        cls = ApproxNumpy
    elif _is_sequence_like(expected):
        cls = ApproxSequenceLike
    elif isinstance(expected, Collection) and not isinstance(expected, str | bytes):
        msg = f"pytest.approx() only supports ordered sequences, but got: {expected!r}"
        raise TypeError(msg)
    elif isinstance(expected, (datetime, timedelta)):
        cls = ApproxTimedelta
    else:
        cls = ApproxScalar

    return cls(expected, rel, abs, nan_ok)


def approx(a, b, fill_value=True, rtol=1e-5, atol=1e-8):
    """
    Returns true if all components of a and b are equal to given tolerances.

    If fill_value is True, masked values considered equal. Otherwise,
    masked values are considered unequal.  The relative error rtol should
    be positive and << 1.0 The absolute error atol comes into play for
    those elements of b that are very small or zero; it says how small a
    must be also.

    """
    m = mask_or(getmask(a), getmask(b))
    d1 = filled(a)
    d2 = filled(b)
    if d1.dtype.char == "O" or d2.dtype.char == "O":
        return np.equal(d1, d2).ravel()
    x = filled(
        masked_array(d1, copy=False, mask=m), fill_value
    ).astype(np.float64)
    y = filled(masked_array(d2, copy=False, mask=m), 1).astype(np.float64)
    d = np.less_equal(umath.absolute(x - y), atol + rtol * umath.absolute(y))
    return d.ravel()

