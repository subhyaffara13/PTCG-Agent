
def test_sort():
    assert sort(str)(Basic(S(3), S(1), S(2))) == Basic(S(1), S(2), S(3))


def test_sort():
    # https://stackoverflow.com/questions/23814368/sorting-pandas-
    #        categorical-labels-after-groupby
    # This should result in a properly sorted Series so that the plot
    # has a sorted x axis
    # self.cat.groupby(['value_group'])['value_group'].count().plot(kind='bar')

    df = DataFrame({"value": np.random.default_rng(2).integers(0, 10000, 10)})
    labels = [f"{i} - {i + 499}" for i in range(0, 10000, 500)]
    cat_labels = Categorical(labels, labels)

    df = df.sort_values(by=["value"], ascending=True)
    df["value_group"] = pd.cut(
        df.value, range(0, 10500, 500), right=False, labels=cat_labels
    )

    res = df.groupby(["value_group"], observed=False)["value_group"].count()
    exp = res[sorted(res.index, key=lambda x: float(x.split()[0]))]
    exp.index = CategoricalIndex(exp.index, name=exp.index.name)
    tm.assert_series_equal(res, exp)


def test_sort(dtype, strings):
    """Test that sorting matches python's internal sorting."""

    def test_sort(strings, arr_sorted):
        arr = np.array(strings, dtype=dtype)
        na_object = getattr(arr.dtype, "na_object", "")
        if na_object is None and None in strings:
            with pytest.raises(
                ValueError,
                match="Cannot compare null that is not a nan-like value",
            ):
                np.argsort(arr)
            argsorted = None
        elif na_object is pd_NA or na_object != '':
            argsorted = None
        else:
            argsorted = np.argsort(arr)
        np.random.default_rng().shuffle(arr)
        if na_object is None and None in strings:
            with pytest.raises(
                ValueError,
                match="Cannot compare null that is not a nan-like value",
            ):
                arr.sort()
        else:
            arr.sort()
            assert np.array_equal(arr, arr_sorted, equal_nan=True)
        if argsorted is not None:
            assert np.array_equal(argsorted, np.argsort(strings))

    # make a copy so we don't mutate the lists in the fixture
    strings = strings.copy()
    arr_sorted = np.array(sorted(strings), dtype=dtype)
    test_sort(strings, arr_sorted)

    if not hasattr(dtype, "na_object"):
        return

    # make sure NAs get sorted to the end of the array and string NAs get
    # sorted like normal strings
    strings.insert(0, dtype.na_object)
    strings.insert(2, dtype.na_object)
    # can't use append because doing that with NA converts
    # the result to object dtype
    if not isinstance(dtype.na_object, str):
        arr_sorted = np.array(
            arr_sorted.tolist() + [dtype.na_object, dtype.na_object],
            dtype=dtype,
        )
    else:
        arr_sorted = np.array(sorted(strings), dtype=dtype)

    test_sort(strings, arr_sorted)

