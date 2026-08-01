
def groupby(
    iterable: Iterable[T] | AsyncIterable[T],
) -> AsyncGenerator[tuple[T, list[T]], None]: ...


def groupby(
    iterable: Iterable[T] | AsyncIterable[T],
    key: Callable[[T], Awaitable[R]],
) -> AsyncGenerator[tuple[R, list[T]], None]: ...


def groupby(key, seq):
    """ Group a collection by a key function

    >>> names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
    >>> groupby(len, names)  # doctest: +SKIP
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}

    >>> iseven = lambda x: x % 2 == 0
    >>> groupby(iseven, [1, 2, 3, 4, 5, 6, 7, 8])  # doctest: +SKIP
    {False: [1, 3, 5, 7], True: [2, 4, 6, 8]}

    Non-callable keys imply grouping on a member.

    >>> groupby('gender', [{'name': 'Alice', 'gender': 'F'},
    ...                    {'name': 'Bob', 'gender': 'M'},
    ...                    {'name': 'Charlie', 'gender': 'M'}]) # doctest:+SKIP
    {'F': [{'gender': 'F', 'name': 'Alice'}],
     'M': [{'gender': 'M', 'name': 'Bob'},
           {'gender': 'M', 'name': 'Charlie'}]}

    Not to be confused with ``itertools.groupby``

    See Also:
        countby
    """
    if not callable(key):
        key = getter(key)
    d = collections.defaultdict(lambda: [].append)
    for item in seq:
        d[key(item)](item)
    rv = {}
    for k, v in d.items():
        rv[k] = v.__self__
    return rv


def groupby(key, seq):
    """Group a collection by a key function

    >>> names = ["Alice", "Bob", "Charlie", "Dan", "Edith", "Frank"]
    >>> groupby(len, names)  # doctest: +SKIP
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}

    >>> iseven = lambda x: x % 2 == 0
    >>> groupby(iseven, [1, 2, 3, 4, 5, 6, 7, 8])  # doctest: +SKIP
    {False: [1, 3, 5, 7], True: [2, 4, 6, 8]}

    Non-callable keys imply grouping on a member.

    >>> groupby(
    ...     "gender",
    ...     [
    ...         {"name": "Alice", "gender": "F"},
    ...         {"name": "Bob", "gender": "M"},
    ...         {"name": "Charlie", "gender": "M"},
    ...     ],
    ... )  # doctest:+SKIP
    {'F': [{'gender': 'F', 'name': 'Alice'}],
     'M': [{'gender': 'M', 'name': 'Bob'},
           {'gender': 'M', 'name': 'Charlie'}]}

    Not to be confused with ``itertools.groupby``

    See Also:
        countby
    """
    if not callable(key):
        key = getter(key)
    d = collections.defaultdict(lambda: [].append)  # type: ignore[var-annotated]
    for item in seq:
        d[key(item)](item)
    rv = {}
    for k, v in d.items():
        rv[k] = v.__self__  # type: ignore[var-annotated, attr-defined]
    return rv


def groupby(func, seq):
    """Group a collection by a key function
    >>> names = ["Alice", "Bob", "Charlie", "Dan", "Edith", "Frank"]
    >>> groupby(len, names)  # doctest: +SKIP
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}
    >>> iseven = lambda x: x % 2 == 0
    >>> groupby(iseven, [1, 2, 3, 4, 5, 6, 7, 8])  # doctest: +SKIP
    {False: [1, 3, 5, 7], True: [2, 4, 6, 8]}
    See Also:
        ``countby``
    """

    d = OrderedDict()  # type: ignore[var-annotated]
    for item in seq:
        key = func(item)
        if key not in d:
            d[key] = []
        d[key].append(item)
    return d


def groupby(func, seq):
    """ Group a collection by a key function

    >>> from sympy.multipledispatch.utils import groupby
    >>> names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
    >>> groupby(len, names)  # doctest: +SKIP
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}

    >>> iseven = lambda x: x % 2 == 0
    >>> groupby(iseven, [1, 2, 3, 4, 5, 6, 7, 8])  # doctest: +SKIP
    {False: [1, 3, 5, 7], True: [2, 4, 6, 8]}

    See Also:
        ``countby``
    """

    d = {}
    for item in seq:
        key = func(item)
        if key not in d:
            d[key] = []
        d[key].append(item)
    return d


def groupby(
    iterable: Iterable[_Tin],
    *,
    key: Callable[[_Tin], _K],
    value: Callable[[_Tin], _Tout] = _identity,
) -> dict[_K, list[_Tout]]:
  """Similar to `itertools.groupby` but return result as a `dict()`.

  Example:

  ```python
  out = epy.groupby(
      ['555', '4', '11', '11', '333'],
      key=len,
      value=int,
  )
  # Order is consistent with above
  assert out == {
      3: [555, 333],
      1: [4],
      2: [11, 11],
  }
  ```

  Other difference with `itertools.groupby`:

   * Iterable do not need to be sorted. Order of the original iterator is
     preserved in the group.
   * Transformation can be applied to the value too

  Args:
    iterable: The iterable to group
    key: Mapping applied to group the values (should return a hashable)
    value: Mapping applied to the values

  Returns:
    The dict
  """
  groups = collections.defaultdict(list)
  for v in iterable:
    groups[key(v)].append(value(v))
  return dict(groups)

