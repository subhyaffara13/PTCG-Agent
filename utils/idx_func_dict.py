
def idx_func_dict():
    return {
        "i": lambda n: Index(np.arange(n), dtype=np.int64),
        "f": lambda n: Index(np.arange(n), dtype=np.float64),
        "s": lambda n: Index([f"{i}_{chr(i)}" for i in range(97, 97 + n)]),
        "dt": lambda n: date_range("2020-01-01", periods=n),
        "td": lambda n: timedelta_range("1 day", periods=n),
        "p": lambda n: period_range("2020-01-01", periods=n, freq="D"),
    }

