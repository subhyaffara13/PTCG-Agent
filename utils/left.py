
def left():
    return DataFrame(
        {
            "X": Series(
                np.random.default_rng(2).choice(["foo", "bar"], size=(10,))
            ).astype(CategoricalDtype(["foo", "bar"])),
            "Y": np.random.default_rng(2).choice(["one", "two", "three"], size=(10,)),
        }
    )


def left():
    return DataFrame({"key": ["a", "c", "e"], "lvalue": [1, 2.0, 3]})


def left():
    """left dataframe (not multi-indexed) for multi-index join tests"""
    # a little relevant example with NAs
    key1 = ["bar", "bar", "bar", "foo", "foo", "baz", "baz", "qux", "qux", "snap"]
    key2 = ["two", "one", "three", "one", "two", "one", "two", "two", "three", "one"]

    data = np.random.default_rng(2).standard_normal(len(key1))
    return DataFrame({"key1": key1, "key2": key2, "data": data})

