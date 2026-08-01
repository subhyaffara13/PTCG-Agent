
def unique_in_window(iterable, n, key=None):
    """Yield the items from *iterable* that haven't been seen recently.
    *n* is the size of the lookback window.

        >>> iterable = [0, 1, 0, 2, 3, 0]
        >>> n = 3
        >>> list(unique_in_window(iterable, n))
        [0, 1, 2, 3, 0]

    The *key* function, if provided, will be used to determine uniqueness:

        >>> list(unique_in_window('abAcda', 3, key=lambda x: x.lower()))
        ['a', 'b', 'c', 'd', 'a']

    The items in *iterable* must be hashable.

    """
    if n <= 0:
        raise ValueError('n must be greater than 0')

    window = deque(maxlen=n)
    counts = defaultdict(int)
    use_key = key is not None

    for item in iterable:
        if len(window) == n:
            to_discard = window[0]
            if counts[to_discard] == 1:
                del counts[to_discard]
            else:
                counts[to_discard] -= 1

        k = key(item) if use_key else item
        if k not in counts:
            yield item
        counts[k] += 1
        window.append(k)

