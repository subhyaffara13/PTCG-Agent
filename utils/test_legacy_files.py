
def test_legacy_files(datapath, legacy_file, using_infer_string, request):
    legacy_version = Version(legacy_file.parent.name)
    legacy_file = datapath(legacy_file)

    if not np_version_gt2 and legacy_file.endswith("fixed.h5"):
        # Files created for versions 2.0-3.0 used a numpy version >= 2.0, and
        # unpickling the object dtype column fails with older numpy
        pytest.skip("Fixed format pickle objects don't deserialize with numpy < 2.0")

    result = pd.read_hdf(legacy_file)

    expected = create_dataframe_all_types()

    # the fixed format doesn't include categorical columns (not supported)
    if legacy_file.endswith("fixed.h5"):
        expected = expected.drop(
            # columns=["categorical", "categorical_object", "categorical_int"]
            columns=["categorical_int"]
        )

    # # object dtype columns with strings get read as `str`
    # if using_infer_string:
    #     expected["object"] = expected["object"].astype("str")
    #     expected["object_nan"] = expected["object_nan"].astype("str")
    #     if legacy_file.endswith("table.h5"):
    #         expected["categorical_object"] = expected["categorical_object"].astype(
    #             pd.CategoricalDtype(
    #                 expected["categorical_object"].cat.categories.astype("str")
    #             )
    #         )
    # else:
    #     expected["string"] = expected["string"].astype("object")
    #     if legacy_file.endswith("table.h5"):
    #         expected["object"] = expected["object"].fillna(np.nan)
    #         expected["categorical"] = expected["categorical"].astype(
    #             pd.CategoricalDtype(
    #                 expected["categorical"].cat.categories.astype(object)
    #             )
    #         )
    #     else:
    #         expected["string"] = expected["string"].fillna("nan")

    if legacy_version < Version("2.2.0") or (
        legacy_version < Version("3.0.0") and legacy_file.endswith("fixed.h5")
    ):
        # timedelta columns gets read as nanoseconds, resulting in buggy values
        # (this also happened for direct roundtrips with those versions)
        assert not result["timedelta_us"].equals(expected["timedelta_us"])
        assert not result["timedelta_ms"].equals(expected["timedelta_ms"])
        assert not result["timedelta_s"].equals(expected["timedelta_s"])
        result = result.drop(columns=["timedelta_us", "timedelta_ms", "timedelta_s"])
        expected = expected.drop(
            columns=["timedelta_us", "timedelta_ms", "timedelta_s"]
        )

    if legacy_version < Version("2.2.0"):
        # datetime columns gets read as nanoseconds, resulting in buggy values
        # (this also happened for direct roundtrips with those versions)
        assert not result["datetime_us"].equals(expected["datetime_us"])
        assert not result["datetime_ms"].equals(expected["datetime_ms"])
        assert not result["datetime_s"].equals(expected["datetime_s"])
        assert not result["datetimetz_us"].equals(expected["datetimetz_us"])
        result = result.drop(
            columns=["datetime_us", "datetime_ms", "datetime_s", "datetimetz_us"]
        )
        expected = expected.drop(
            columns=["datetime_us", "datetime_ms", "datetime_s", "datetimetz_us"]
        )

    tm.assert_frame_equal(result, expected)

