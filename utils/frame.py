
def frame():
    """Make mocked frame as fixture."""
    return DataFrame(
        np.random.default_rng(2).standard_normal((100, 10)),
        index=bdate_range(datetime(2009, 1, 1), periods=100),
    )


def frame(float_frame):
    """
    Returns the first ten items in fixture "float_frame".
    """
    return float_frame[:10]


def frame():
    floating = Series(np.random.default_rng(2).standard_normal(10))
    floating_missing = floating.copy()
    floating_missing.iloc[2:7] = np.nan
    strings = list("abcde") * 2
    strings_missing = strings[:]
    strings_missing[5] = np.nan

    df = DataFrame(
        {
            "float": floating,
            "float_missing": floating_missing,
            "int": [1, 1, 1, 1, 2] * 2,
            "datetime": date_range("1990-1-1", periods=10),
            "timedelta": pd.timedelta_range(1, freq="s", periods=10),
            "string": strings,
            "string_missing": strings_missing,
            "cat": Categorical(strings),
        },
    )
    return df

