
def test_map(doc):
    """std::map <-> dict"""
    d = m.cast_map()
    assert d == {"key": "value"}
    assert "key" in d
    d["key2"] = "value2"
    assert "key2" in d
    assert m.load_map(d)

    assert doc(m.cast_map) == "cast_map() -> Dict[str, str]"
    assert doc(m.load_map) == "load_map(arg0: Dict[str, str]) -> bool"


def test_map():
    data = {
        "A": [0.0, 1.0, 2.0, 3.0, 4.0],
        "B": [0.0, 1.0, 0.0, 1.0, 0.0],
        "C": ["foo1", "foo2", "foo3", "foo4", "foo5"],
        "D": bdate_range("1/1/2009", periods=5),
    }

    source = Series(data["B"], index=data["C"])
    target = Series(data["C"][:4], index=data["D"][:4])

    merged = target.map(source)

    for k, v in merged.items():
        assert v == source[target[k]]

    # input could be a dict
    merged = target.map(source.to_dict())

    for k, v in merged.items():
        assert v == source[target[k]]


def test_map():
    ci = CategoricalIndex(list("ABABC"), categories=list("CBA"), ordered=True)
    result = ci.map(lambda x: x.lower())
    exp = CategoricalIndex(list("ababc"), categories=list("cba"), ordered=True)
    tm.assert_index_equal(result, exp)

    ci = CategoricalIndex(
        list("ABABC"), categories=list("BAC"), ordered=False, name="XXX"
    )
    result = ci.map(lambda x: x.lower())
    exp = CategoricalIndex(
        list("ababc"), categories=list("bac"), ordered=False, name="XXX"
    )
    tm.assert_index_equal(result, exp)

    # GH 12766: Return an index not an array
    tm.assert_index_equal(
        ci.map(lambda x: 1), Index(np.array([1] * 5, dtype=np.int64), name="XXX")
    )

    # change categories dtype
    ci = CategoricalIndex(list("ABABC"), categories=list("BAC"), ordered=False)

    def f(x):
        return {"A": 10, "B": 20, "C": 30}.get(x)

    result = ci.map(f)
    exp = CategoricalIndex([10, 20, 10, 20, 30], categories=[20, 10, 30], ordered=False)
    tm.assert_index_equal(result, exp)

    result = ci.map(Series([10, 20, 30], index=["A", "B", "C"]))
    tm.assert_index_equal(result, exp)

    result = ci.map({"A": 10, "B": 20, "C": 30})
    tm.assert_index_equal(result, exp)


def test_map(idx):
    # callable
    index = idx

    result = index.map(lambda x: x)
    tm.assert_index_equal(result, index)


def test_map(float_frame):
    result = float_frame.map(lambda x: x * 2)
    tm.assert_frame_equal(result, float_frame * 2)
    float_frame.map(type)

    # GH 465: function returning tuples
    result = float_frame.map(lambda x: (x, x))["A"].iloc[0]
    assert isinstance(result, tuple)


def test_map(na_action):
    cat = Categorical(list("ABABC"), categories=list("CBA"), ordered=True)
    result = cat.map(lambda x: x.lower(), na_action=na_action)
    exp = Categorical(list("ababc"), categories=list("cba"), ordered=True)
    tm.assert_categorical_equal(result, exp)

    cat = Categorical(list("ABABC"), categories=list("BAC"), ordered=False)
    result = cat.map(lambda x: x.lower(), na_action=na_action)
    exp = Categorical(list("ababc"), categories=list("bac"), ordered=False)
    tm.assert_categorical_equal(result, exp)

    # GH 12766: Return an index not an array
    result = cat.map(lambda x: 1, na_action=na_action)
    exp = Index(np.array([1] * 5, dtype=np.int64))
    tm.assert_index_equal(result, exp)

    # change categories dtype
    cat = Categorical(list("ABABC"), categories=list("BAC"), ordered=False)

    def f(x):
        return {"A": 10, "B": 20, "C": 30}.get(x)

    result = cat.map(f, na_action=na_action)
    exp = Categorical([10, 20, 10, 20, 30], categories=[20, 10, 30], ordered=False)
    tm.assert_categorical_equal(result, exp)

    mapper = Series([10, 20, 30], index=["A", "B", "C"])
    result = cat.map(mapper, na_action=na_action)
    tm.assert_categorical_equal(result, exp)

    result = cat.map({"A": 10, "B": 20, "C": 30}, na_action=na_action)
    tm.assert_categorical_equal(result, exp)


def test_map():
    arr = SparseArray([0, 1, 2])
    expected = SparseArray([10, 11, 12], fill_value=10)

    # dict
    result = arr.map({0: 10, 1: 11, 2: 12})
    tm.assert_sp_array_equal(result, expected)

    # series
    result = arr.map(pd.Series({0: 10, 1: 11, 2: 12}))
    tm.assert_sp_array_equal(result, expected)

    # function
    result = arr.map(pd.Series({0: 10, 1: 11, 2: 12}))
    expected = SparseArray([10, 11, 12], fill_value=10)
    tm.assert_sp_array_equal(result, expected)

