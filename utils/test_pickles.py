from pathlib import Path


def test_pickles(datapath):
    pytest.importorskip("pytz")
    if not is_platform_little_endian():
        pytest.skip("known failure on non-little endian")

    current_data = create_pickle_data()

    # For loop for compat with --strict-data-files
    for legacy_pickle in Path(__file__).parent.glob("data/legacy_pickle/*/*.p*kl*"):
        legacy_version = Version(legacy_pickle.parent.name)
        legacy_pickle = datapath(legacy_pickle)

        data = pd.read_pickle(legacy_pickle)

        for typ, dv in data.items():
            for dt, result in dv.items():
                expected = current_data[typ][dt]

                if (
                    typ == "timestamp"
                    and dt in ("tz", "both")
                    and legacy_version < Version("1.3.0")
                ):
                    # convert to wall time
                    # (bug since pandas 2.0 that tz gets dropped for older pickle files)
                    expected = expected.tz_convert(None)

                if legacy_version < Version("3.0.0.dev0"):
                    # before 3.0, we had:
                    # - object dtype instead of string
                    # - ns instead of us as the default unit
                    if typ in ("frame", "sp_frame"):
                        expected.columns = expected.columns.astype("object")
                        if dt in ("mixed", "mixed_dup"):
                            expected["C"] = expected["C"].astype(object)
                            expected["D"] = expected["D"].dt.as_unit("ns")
                        elif dt in ("cat_onecol", "cat_and_float"):
                            expected["A"] = expected["A"].astype(
                                pd.CategoricalDtype(
                                    expected["A"].cat.categories.astype(object)
                                )
                            )
                        elif typ == "sp_frame" and dt == "float":
                            expected.index = expected.index.as_unit("ns")
                        elif dt == "mi":
                            expected.index = expected.index.set_levels(
                                [
                                    level.astype("object")
                                    for level in expected.index.levels
                                ],
                            )
                    elif typ in ("series", "sp_series"):
                        if dt == "ts":
                            expected.index = expected.index.as_unit("ns")
                        elif dt in ("dt", "dt_tz"):
                            expected = expected.dt.as_unit("ns")
                        elif dt == "cat":
                            expected = expected.astype(
                                pd.CategoricalDtype(
                                    expected.cat.categories.astype(object)
                                )
                            )
                        elif dt == "dup":
                            expected.index = expected.index.astype(object)
                    elif typ == "index" and dt in ("date", "timedelta"):
                        expected = expected.as_unit("ns")
                    elif typ == "mi":
                        expected = expected.set_levels(
                            [level.astype("object") for level in expected.levels],
                        )
                    if dt == "string":
                        # we switched from python to pyarrow as default storage in 3.0
                        expected = expected.astype(pd.StringDtype("python"))

                if dt in ("dt_mixed_tzs", "dt_mixed2_tzs"):
                    if legacy_version < Version("2.1"):
                        # in pandas < 2.0, Timestamp() unit defaulted to 'ns'
                        expected_unit = "ns"
                    elif Version("2.1") <= legacy_version < Version("3.0.0.dev0"):
                        # in pandas 2.x, Timestamp() unit depended on input
                        expected_unit = "s"
                    else:
                        expected_unit = "us"
                    for col in expected.columns:
                        expected[col] = expected[col].dt.as_unit(expected_unit)
                if typ == "index" and dt == "int" and "windows" in legacy_pickle:
                    expected = expected.astype(np.int32)

                if typ == "series" and dt == "ts":
                    # GH 7748
                    tm.assert_series_equal(result, expected)
                    assert result.index.freq == expected.index.freq
                    assert not result.index.freq.normalize
                    tm.assert_series_equal(result > 0, expected > 0)

                    # GH 9291
                    freq = result.index.freq
                    assert freq + Day(1) == Day(2)

                    res = freq + pd.Timedelta(hours=1)
                    assert isinstance(res, pd.Timedelta)
                    assert res == pd.Timedelta(days=1, hours=1)

                    res = freq + pd.Timedelta(nanoseconds=1)
                    assert isinstance(res, pd.Timedelta)
                    assert res == pd.Timedelta(days=1, nanoseconds=1)
                elif typ == "index" and dt == "period":
                    tm.assert_index_equal(result, expected)
                    assert isinstance(result.freq, MonthEnd)
                    assert result.freq == MonthEnd()
                    assert result.freqstr == "M"
                    tm.assert_index_equal(result.shift(2), expected.shift(2))
                elif typ == "series" and dt in ("dt_tz", "cat"):
                    tm.assert_series_equal(result, expected)
                elif typ == "frame" and dt in (
                    "dt_mixed_tzs",
                    "cat_onecol",
                    "cat_and_float",
                ):
                    tm.assert_frame_equal(result, expected)
                else:
                    compare_element(result, expected, typ)

