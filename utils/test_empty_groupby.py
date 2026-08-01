
def test_empty_groupby(columns, keys, values, method, op, dropna, using_infer_string):
    # GH8093 & GH26411
    override_dtype = None

    if isinstance(values, BooleanArray) and op in ["sum", "prod"]:
        # We expect to get Int64 back for these
        override_dtype = "Int64"

    if isinstance(values[0], bool) and op in ("prod", "sum"):
        # sum/product of bools is an integer
        override_dtype = "int64"

    df = DataFrame({"A": values, "B": values, "C": values}, columns=list("ABC"))

    if hasattr(values, "dtype"):
        # check that we did the construction right
        assert (df.dtypes == values.dtype).all()

    df = df.iloc[:0]

    gb = df.groupby(keys, group_keys=False, dropna=dropna, observed=False)[columns]

    def get_result(**kwargs):
        if method == "attr":
            return getattr(gb, op)(**kwargs)
        else:
            return getattr(gb, method)(op, **kwargs)

    def get_categorical_invalid_expected():
        # Categorical is special without 'observed=True', we get a NaN entry
        #  corresponding to the unobserved group. If we passed observed=True
        #  to groupby, expected would just be 'df.set_index(keys)[columns]'
        #  as below
        lev = Categorical([0], dtype=values.dtype)
        if len(keys) != 1:
            idx = MultiIndex.from_product([lev, lev], names=keys)
        else:
            # all columns are dropped, but we end up with one row
            # Categorical is special without 'observed=True'
            idx = Index(lev, name=keys[0])

        if using_infer_string:
            columns = Index([], dtype="str")
        else:
            columns = []
        expected = DataFrame([], columns=columns, index=idx)
        return expected

    is_per = isinstance(df.dtypes.iloc[0], pd.PeriodDtype)
    is_dt64 = df.dtypes.iloc[0].kind == "M"
    is_cat = isinstance(values, Categorical)
    is_str = isinstance(df.dtypes.iloc[0], pd.StringDtype)

    if (
        isinstance(values, Categorical)
        and not values.ordered
        and op in ["min", "max", "idxmin", "idxmax"]
    ):
        if op in ["min", "max"]:
            msg = f"Cannot perform {op} with non-ordered Categorical"
            klass = TypeError
        else:
            msg = f"Can't get {op} of an empty group due to unobserved categories"
            klass = ValueError
        with pytest.raises(klass, match=msg):
            get_result()

        if op in ["min", "max", "idxmin", "idxmax"] and isinstance(columns, list):
            # i.e. DataframeGroupBy, not SeriesGroupBy
            result = get_result(numeric_only=True)
            expected = get_categorical_invalid_expected()
            tm.assert_equal(result, expected)
        return

    if op in ["prod", "sum", "skew", "kurt"]:
        # ops that require more than just ordered-ness
        if is_dt64 or is_cat or is_per or (is_str and op != "sum"):
            # GH#41291
            # datetime64 -> prod and sum are invalid
            if is_dt64:
                msg = "datetime64 type does not support"
            elif is_per:
                msg = "Period type does not support"
            elif is_str:
                msg = f"dtype 'str' does not support operation '{op}'"
            else:
                msg = "category type does not support"
            if op in ["skew", "kurt"]:
                msg = "|".join([msg, f"does not support operation '{op}'"])
            with pytest.raises(TypeError, match=msg):
                get_result()

            if not isinstance(columns, list):
                # i.e. SeriesGroupBy
                return
            elif op in ["skew", "kurt"]:
                # TODO: test the numeric_only=True case
                return
            else:
                # i.e. op in ["prod", "sum"]:
                # i.e. DataFrameGroupBy
                # ops that require more than just ordered-ness
                # GH#41291
                result = get_result(numeric_only=True)

                # with numeric_only=True, these are dropped, and we get
                # an empty DataFrame back
                expected = df.set_index(keys)[[]]
                if is_cat:
                    expected = get_categorical_invalid_expected()
                tm.assert_equal(result, expected)
                return

    result = get_result()
    expected = df.set_index(keys)[columns]
    if op in ["idxmax", "idxmin"]:
        expected = expected.astype(df.index.dtype)
    if override_dtype is not None:
        expected = expected.astype(override_dtype)
    if len(keys) == 1:
        expected.index.name = keys[0]
    tm.assert_equal(result, expected)

