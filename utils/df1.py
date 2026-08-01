
def df1():
    return DataFrame(
        {
            "int": [1, 3],
            "float": [2.0, np.nan],
            "str": ["t", "s"],
            "dt": date_range("2018-06-18", periods=2),
        }
    )


def df1():
    res = DataFrame(
        [
            [1.067683, -1.110463, 0.20867],
            [-1.321405, 0.368915, -1.055342],
            [-0.807333, 0.08298, -0.873361],
        ]
    )
    res.columns = [list("ABC"), list("abc")]
    res.columns.names = ["CAP", "low"]
    return res


def df1():
    return DataFrame(
        {
            "outer": [1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4],
            "inner": [1, 2, 3, 1, 2, 3, 4, 1, 2, 1, 2],
            "v1": np.linspace(0, 1, 11),
        }
    )

