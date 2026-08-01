
def test_interchange_from_non_pandas_tz_aware(request):
    # GH 54239, 54287
    pa = pytest.importorskip("pyarrow", "11.0.0")
    import pyarrow.compute as pc

    if is_platform_windows() and is_ci_environment() and pa_version_under22p0:
        mark = pytest.mark.xfail(
            raises=pa.ArrowInvalid,
            reason=(
                "TODO: Set ARROW_TIMEZONE_DATABASE environment variable "
                "on CI to path to the tzdata for pyarrow."
            ),
        )
        request.applymarker(mark)

    arr = pa.array([datetime(2020, 1, 1), None, datetime(2020, 1, 2)])
    arr = pc.assume_timezone(arr, "Asia/Kathmandu")
    table = pa.table({"arr": arr})
    exchange_df = table.__dataframe__()
    with tm.assert_produces_warning(match="Interchange"):
        result = from_dataframe(exchange_df)

    expected = pd.DataFrame(
        ["2020-01-01 00:00:00+05:45", "NaT", "2020-01-02 00:00:00+05:45"],
        columns=["arr"],
        dtype="datetime64[us, Asia/Kathmandu]",
    )
    tm.assert_frame_equal(expected, result)

