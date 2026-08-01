
def test_len_categorical(dropna, observed, keys):
    # GH#57595
    df = DataFrame(
        {
            "a": Categorical([1, 1, 2, np.nan], categories=[1, 2, 3]),
            "b": Categorical([1, 1, 2, np.nan], categories=[1, 2, 3]),
            "c": 1,
        }
    )
    gb = df.groupby(keys, observed=observed, dropna=dropna)
    result = len(gb)
    if observed and dropna:
        expected = 2
    elif observed and not dropna:
        expected = 3
    elif len(keys) == 1:
        expected = 3 if dropna else 4
    else:
        expected = 9 if dropna else 16
    assert result == expected, f"{result} vs {expected}"

