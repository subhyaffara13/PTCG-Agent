
def test_astype_dispatches(frame_or_series):
    # This is a dtype-specific test that ensures Series[decimal].astype
    # gets all the way through to ExtensionArray.astype
    # Designing a reliable smoke test that works for arbitrary data types
    # is difficult.
    data = pd.Series(DecimalArray([decimal.Decimal(2)]), name="a")
    ctx = decimal.Context()
    ctx.prec = 5

    data = frame_or_series(data)

    result = data.astype(DecimalDtype(ctx))

    if frame_or_series is pd.DataFrame:
        result = result["a"]

    assert result.dtype.context.prec == ctx.prec

