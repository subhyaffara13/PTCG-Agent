from typing import Any

def replace(pattern):
    r"""
    >>> replace(r'foo\z')
    'foo\\Z'
    """
    return pattern[:-2] + pattern[-2:].replace(r'\z', r'\Z')


def replace(string, *reps):
    """Return ``string`` with all keys in ``reps`` replaced with
    their corresponding values, longer strings first, irrespective
    of the order they are given.  ``reps`` may be passed as tuples
    or a single mapping.

    Examples
    ========

    >>> from sympy.utilities.misc import replace
    >>> replace('foo', {'oo': 'ar', 'f': 'b'})
    'bar'
    >>> replace("spamham sha", ("spam", "eggs"), ("sha","md5"))
    'eggsham md5'

    There is no guarantee that a unique answer will be
    obtained if keys in a mapping overlap (i.e. are the same
    length and have some identical sequence at the
    beginning/end):

    >>> reps = [
    ...     ('ab', 'x'),
    ...     ('bc', 'y')]
    >>> replace('abc', *reps) in ('xc', 'ay')
    True

    References
    ==========

    .. [1] https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
    """
    if len(reps) == 1:
        kv = reps[0]
        if isinstance(kv, dict):
            reps = kv
        else:
            return string.replace(*kv)
    else:
        reps = dict(reps)
    return _replace(reps)(string)


def replace(iterable, pred, substitutes, count=None, window_size=1):
    """Yield the items from *iterable*, replacing the items for which *pred*
    returns ``True`` with the items from the iterable *substitutes*.

        >>> iterable = [1, 1, 0, 1, 1, 0, 1, 1]
        >>> pred = lambda x: x == 0
        >>> substitutes = (2, 3)
        >>> list(replace(iterable, pred, substitutes))
        [1, 1, 2, 3, 1, 1, 2, 3, 1, 1]

    If *count* is given, the number of replacements will be limited:

        >>> iterable = [1, 1, 0, 1, 1, 0, 1, 1, 0]
        >>> pred = lambda x: x == 0
        >>> substitutes = [None]
        >>> list(replace(iterable, pred, substitutes, count=2))
        [1, 1, None, 1, 1, None, 1, 1, 0]

    Use *window_size* to control the number of items passed as arguments to
    *pred*. This allows for locating and replacing subsequences.

        >>> iterable = [0, 1, 2, 5, 0, 1, 2, 5]
        >>> window_size = 3
        >>> pred = lambda *args: args == (0, 1, 2)  # 3 items passed to pred
        >>> substitutes = [3, 4] # Splice in these items
        >>> list(replace(iterable, pred, substitutes, window_size=window_size))
        [3, 4, 5, 3, 4, 5]

    """
    if window_size < 1:
        raise ValueError('window_size must be at least 1')

    # Save the substitutes iterable, since it's used more than once
    substitutes = tuple(substitutes)

    # Add padding such that the number of windows matches the length of the
    # iterable
    it = chain(iterable, repeat(_marker, window_size - 1))
    windows = windowed(it, window_size)

    n = 0
    for w in windows:
        # If the current window matches our predicate (and we haven't hit
        # our maximum number of replacements), splice in the substitutes
        # and then consume the following windows that overlap with this one.
        # For example, if the iterable is (0, 1, 2, 3, 4...)
        # and the window size is 2, we have (0, 1), (1, 2), (2, 3)...
        # If the predicate matches on (0, 1), we need to zap (0, 1) and (1, 2)
        if pred(*w):
            if (count is None) or (n < count):
                n += 1
                yield from substitutes
                consume(windows, window_size - 1)
                continue

        # If there was no match (or we've reached the replacement limit),
        # yield the first item from the window.
        if w and (w[0] is not _marker):
            yield w[0]


def replace(pattern):
    r"""
    >>> replace(r'foo\z')
    'foo\\Z'
    """
    return pattern[:-2] + pattern[-2:].replace(r'\z', r'\Z')


def replace(str, d, defaultsep=''):
    if isinstance(d, list):
        return [replace(str, _m, defaultsep) for _m in d]
    if isinstance(str, list):
        return [replace(_m, d, defaultsep) for _m in str]
    for k in 2 * list(d.keys()):
        if k == 'separatorsfor':
            continue
        if 'separatorsfor' in d and k in d['separatorsfor']:
            sep = d['separatorsfor'][k]
        else:
            sep = defaultsep
        if isinstance(d[k], list):
            str = str.replace(f'#{k}#', sep.join(flatlist(d[k])))
        else:
            str = str.replace(f'#{k}#', d[k])
    return str


def replace(a, old, new, count=-1):
    """
    For each element in ``a``, return a copy of the string with
    occurrences of substring ``old`` replaced by ``new``.

    Parameters
    ----------
    a : array_like, with ``bytes_`` or ``str_`` dtype

    old, new : array_like, with ``bytes_`` or ``str_`` dtype

    count : array_like, with ``int_`` dtype
        If the optional argument ``count`` is given, only the first
        ``count`` occurrences are replaced.

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input types

    See Also
    --------
    str.replace

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(["That is a mango", "Monkeys eat mangos"])
    >>> np.strings.replace(a, 'mango', 'banana')
    array(['That is a banana', 'Monkeys eat bananas'], dtype='<U19')

    >>> a = np.array(["The dish is fresh", "This is it"])
    >>> np.strings.replace(a, 'is', 'was')
    array(['The dwash was fresh', 'Thwas was it'], dtype='<U19')

    """
    count = np.asanyarray(count)
    if not np.issubdtype(count.dtype, np.integer):
        raise TypeError(f"unsupported type {count.dtype} for operand 'count'")

    arr = np.asanyarray(a)
    old_dtype = getattr(old, 'dtype', None)
    old = np.asanyarray(old)
    new_dtype = getattr(new, 'dtype', None)
    new = np.asanyarray(new)

    if np.result_type(arr, old, new).char == "T":
        return _replace(arr, old, new, count)

    a_dt = arr.dtype
    old = old.astype(old_dtype or a_dt, copy=False)
    new = new.astype(new_dtype or a_dt, copy=False)
    max_int64 = np.iinfo(np.int64).max
    counts = _count_ufunc(arr, old, 0, max_int64)
    counts = np.where(count < 0, counts, np.minimum(counts, count))
    buffersizes = str_len(arr) + counts * (str_len(new) - str_len(old))
    out_dtype = f"{arr.dtype.char}{buffersizes.max()}"
    out = np.empty_like(arr, shape=buffersizes.shape, dtype=out_dtype)

    return _replace(arr, old, new, counts, out=out)


def replace(state: StateCore) -> None:
    if not state.md.options.typographer:
        return

    for token in state.tokens:
        if token.type != "inline":
            continue
        if token.children is None:
            continue

        if SCOPED_ABBR_RE.search(token.content):
            replace_scoped(token.children)

        if RARE_RE.search(token.content):
            replace_rare(token.children)


def replace(self: _T, **kwargs: Any) -> _T:
  """Similar to `dataclasses.replace`."""
  return dataclasses.replace(self, **kwargs)

