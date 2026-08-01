
def create_dataframe_all_types():
    timestamps = Series(
        [
            Timestamp("2013-01-01"),
            NaT,
            Timestamp("2013-01-03"),
            Timestamp("2013-01-04"),
            Timestamp("2013-01-05"),
        ]
    )
    timedeltas = timestamps - timestamps[0]

    data = {
        # "string": Series(
        #     ["a", "b", "c", None, "e"], dtype=StringDtype(na_value=np.nan)
        # ),
        # "object": Series(["a", "b", "c", None, "e"], dtype=object),
        # "object_nan": Series(["a", "b", "c", np.nan, "e"], dtype=object),
        "int": list(range(1, 6)),
        "uint64": np.arange(3, 8).astype("uint64"),
        "float": [0.1, 0.2, 0.3, 0.4, np.nan],
        "float32": Series([0.1, 0.2, 0.3, 0.4, np.nan], dtype="float32"),
        "bool": [True, False, True, False, True],
        "datetime_ns": timestamps.dt.as_unit("ns"),
        "datetime_us": timestamps.dt.as_unit("us"),
        "datetime_ms": timestamps.dt.as_unit("ms"),
        "datetime_s": timestamps.dt.as_unit("s"),
        "datetimetz_ns": timestamps.dt.tz_localize("US/Eastern").dt.as_unit("ns"),
        "datetimetz_us": timestamps.dt.tz_localize("US/Eastern").dt.as_unit("us"),
        "timedelta_ns": timedeltas.dt.as_unit("ns"),
        "timedelta_us": timedeltas.dt.as_unit("us"),
        "timedelta_ms": timedeltas.dt.as_unit("ms"),
        "timedelta_s": timedeltas.dt.as_unit("s"),
        # "categorical": Categorical(
        #     Series(
        #         ["foo", "bar", "baz",np.nan,"foo"],dtype=StringDtype(na_value=np.nan)
        #     )
        # ),
        # "categorical_object": Categorical(
        #     Series(["foo", "bar", "baz", np.nan, "foo"], dtype=object)
        # ),
        "categorical_int": Categorical([1, 2, 3, np.nan, 1]),
    }
    return DataFrame(data)

