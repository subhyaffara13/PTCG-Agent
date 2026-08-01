
def df():
    return DataFrame({"A": [1, 2, 3]})


def df():
    """DataFrame with columns 'L1', 'L2', and 'L3'"""
    return pd.DataFrame({"L1": [1, 2, 3], "L2": [11, 12, 13], "L3": ["A", "B", "C"]})


def df():
    return DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
            "C": np.random.default_rng(2).standard_normal(8),
            "D": np.random.default_rng(2).standard_normal(8),
        }
    )


def df():
    return DataFrame(
        {
            "A": np.arange(6, dtype="int64"),
        },
        index=CategoricalIndex(
            list("aabbca"), dtype=CategoricalDtype(list("cab")), name="B"
        ),
    )


def df(request):
    data_type = request.param

    if data_type == "delims":
        return DataFrame({"a": ['"a,\t"b|c', "d\tef`"], "b": ["hi'j", "k''lm"]})
    elif data_type == "utf8":
        return DataFrame({"a": ["µasd", "Ωœ∑`"], "b": ["øπ∆˚¬", "œ∑`®"]})
    elif data_type == "utf16":
        return DataFrame(
            {"a": ["\U0001f44d\U0001f44d", "\U0001f44d\U0001f44d"], "b": ["abc", "def"]}
        )
    elif data_type == "string":
        return DataFrame(
            np.array([f"i-{i}" for i in range(15)]).reshape(5, 3), columns=list("abc")
        )
    elif data_type == "long":
        max_rows = get_option("display.max_rows")
        return DataFrame(
            np.random.default_rng(2).integers(0, 10, size=(max_rows + 1, 3)),
            columns=list("abc"),
        )
    elif data_type == "nonascii":
        return DataFrame({"en": "in English".split(), "es": "en español".split()})
    elif data_type == "colwidth":
        _cw = get_option("display.max_colwidth") + 1
        return DataFrame(
            np.array(["x" * _cw for _ in range(15)]).reshape(5, 3), columns=list("abc")
        )
    elif data_type == "mixed":
        return DataFrame(
            {
                "a": np.arange(1.0, 6.0) + 0.01,
                "b": np.arange(1, 6).astype(np.int64),
                "c": list("abcde"),
            }
        )
    elif data_type == "float":
        return DataFrame(np.random.default_rng(2).random((5, 3)), columns=list("abc"))
    elif data_type == "int":
        return DataFrame(
            np.random.default_rng(2).integers(0, 10, (5, 3)), columns=list("abc")
        )
    else:
        raise ValueError


def df(index):
    frame = DataFrame(
        np.random.default_rng(2).random((10, 2)), columns=list("AB"), index=index
    )
    return frame


def df():
    df = DataFrame(
        {
            "A": [
                "foo",
                "foo",
                "foo",
                "foo",
                "bar",
                "bar",
                "bar",
                "bar",
                "foo",
                "foo",
                "foo",
            ],
            "B": [
                "one",
                "one",
                "one",
                "two",
                "one",
                "one",
                "one",
                "two",
                "two",
                "two",
                "one",
            ],
            "C": [
                "dull",
                "dull",
                "shiny",
                "dull",
                "dull",
                "shiny",
                "shiny",
                "dull",
                "shiny",
                "shiny",
                "shiny",
            ],
            "D": np.random.default_rng(2).standard_normal(11),
            "E": np.random.default_rng(2).standard_normal(11),
            "F": np.random.default_rng(2).standard_normal(11),
        }
    )

    return pd.concat([df, df], ignore_index=True)


def df():
    res = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    res["id1"] = (res["A"] > 0).astype(np.int64)
    res["id2"] = (res["B"] > 0).astype(np.int64)
    return res


def df():
    """
    base dataframe for testing
    """
    return DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})


def df():
    return DataFrame(
        data=[[0, -0.609], [1, -1.228]],
        columns=["A", "B"],
        index=["x", "y"],
    )


def df():
    return DataFrame(
        data=[[0, -0.609], [1, -1.228]],
        columns=["A", "B"],
        index=["x", "y"],
    )


def df(request):
    # GH 45804
    dtype = request.param[1]
    item = np.nan if dtype == "float64" else NA
    return DataFrame(
        {"A": [0, item, 10], "B": [1, request.param[0], 2]}, dtype=request.param[1]
    )


def df():
    return DataFrame([[1, 2], [2, 4]], columns=["A", "B"])


def df():
    return DataFrame(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        index=["i", "j", "j"],
        columns=["c", "d", "d"],
        dtype=float,
    )


def df():
    df = DataFrame({"A": [0, 1], "B": np.random.default_rng(2).standard_normal(2)})
    return df


def df():
    return DataFrame(
        data=[[0, 1, 2], [3, 4, 5], [6, 7, 8]],
        columns=["A", "B", "C"],
        index=["x", "y", "z"],
    )


def df():
    return DataFrame(
        {"A": [0, 1], "B": [-0.61, -1.22], "C": Series(["ab", "cd"], dtype=object)}
    )


def df():
    return DataFrame(
        {"A": [0, 1], "B": [-0.61, -1.22], "C": Series(["ab", "cd"], dtype=object)}
    )


def df():
    return DataFrame(
        {"A": [0, 1], "B": [-0.61, -1.22], "C": Series(["ab", "cd"], dtype=object)}
    )


def df(vals, cols):
    return DataFrame(vals, columns=cols)


def df():
    #                        c1
    # 2016-01-01 00:00:00 a   0
    #                     b   1
    #                     c   2
    # 2016-01-01 12:00:00 a   3
    #                     b   4
    #                     c   5
    # 2016-01-02 00:00:00 a   6
    #                     b   7
    #                     c   8
    # 2016-01-02 12:00:00 a   9
    #                     b  10
    #                     c  11
    # 2016-01-03 00:00:00 a  12
    #                     b  13
    #                     c  14
    dr = date_range("2016-01-01", "2016-01-03", freq="12h")
    abc = ["a", "b", "c"]
    mi = MultiIndex.from_product([dr, abc])
    frame = DataFrame({"c1": range(15)}, index=mi)
    return frame

