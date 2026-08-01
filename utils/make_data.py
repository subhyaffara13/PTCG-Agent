
def make_data(n: int):
    while True:
        values = np.random.default_rng(2).choice(list(string.ascii_letters), size=n)
        # ensure we meet the requirements
        # 1. first two not null
        # 2. first and second are different
        if values[0] != values[1]:
            break
    return values


def make_data(n: int):
    left_array = np.random.default_rng(2).uniform(size=n).cumsum()
    right_array = left_array + np.random.default_rng(2).uniform(size=n)
    return [
        Interval(left, right)
        for left, right in zip(left_array, right_array, strict=True)
    ]


def make_data():
    return [1, 2, 3, 4, pd.NA, 10, 11, pd.NA, 99, 100]


def make_data(fill_value, n: int):
    rng = np.random.default_rng(2)
    if np.isnan(fill_value):
        data = rng.uniform(size=n)
    else:
        data = rng.integers(1, 100, size=n, dtype=int)
        if data[0] == data[1]:
            data[0] += 1

    data[2::3] = fill_value
    return data


def make_data(n: int):
    return [decimal.Decimal(val) for val in np.random.default_rng(2).random(n)]


def make_data(n: int):
    # TODO: Use a regular dict. See _NDFrameIndexer._setitem_with_indexer
    rng = np.random.default_rng(2)
    return [
        UserDict(
            [
                (rng.choice(list(string.ascii_letters)), rng.integers(0, 100))
                for _ in range(rng.integers(0, 10))
            ]
        )
        for _ in range(n)
    ]


def make_data(n: int):
    # TODO: Use a regular dict. See _NDFrameIndexer._setitem_with_indexer
    rng = np.random.default_rng(2)
    data = np.empty(n, dtype=object)
    data[:] = [
        [rng.choice(list(string.ascii_letters)) for _ in range(rng.integers(0, 10))]
        for _ in range(n)
    ]
    return data

