
def test_quantile(method, dtype, xp, devices):
    if (is_array_api_strict(xp) or is_torch(xp)) and method == 'harrell-davis':
        pytest.skip("'harrell-davis' not currently supported on GPU.")

    dtype = getattr(xp, dtype)
    for device in devices:
        values = get_arrays(1, device=device, dtype=dtype, xp=xp)[0]
        res = stats.quantile(values, 0.5, method=method)
        assert xp_device(res) == xp_device(values)
        assert values.dtype == dtype


def test_quantile(data, interpolation, quantile, request):
    pa_dtype = data.dtype.pyarrow_dtype

    data = data.take([0, 0, 0])
    ser = pd.Series(data)

    if (
        pa.types.is_string(pa_dtype)
        or pa.types.is_binary(pa_dtype)
        or pa.types.is_boolean(pa_dtype)
    ):
        # For string, bytes, and bool, we don't *expect* to have quantile work
        # Note this matches the non-pyarrow behavior
        msg = r"Function 'quantile' has no kernel matching input types \(.*\)"
        with pytest.raises(pa.ArrowNotImplementedError, match=msg):
            ser.quantile(q=quantile, interpolation=interpolation)
        return

    if (
        pa.types.is_integer(pa_dtype)
        or pa.types.is_floating(pa_dtype)
        or pa.types.is_decimal(pa_dtype)
    ):
        pass
    elif pa.types.is_temporal(data._pa_array.type):
        pass
    else:
        request.applymarker(
            pytest.mark.xfail(
                raises=pa.ArrowNotImplementedError,
                reason=f"quantile not supported by pyarrow for {pa_dtype}",
            )
        )
    data = data.take([0, 0, 0])
    ser = pd.Series(data)
    result = ser.quantile(q=quantile, interpolation=interpolation)

    if pa.types.is_timestamp(pa_dtype) and interpolation not in ["lower", "higher"]:
        # rounding error will make the check below fail
        #  (e.g. '2020-01-01 01:01:01.000001' vs '2020-01-01 01:01:01.000001024'),
        #  so we'll check for now that we match the numpy analogue
        if pa_dtype.tz:
            pd_dtype = f"M8[{pa_dtype.unit}, {pa_dtype.tz}]"
        else:
            pd_dtype = f"M8[{pa_dtype.unit}]"
        ser_np = ser.astype(pd_dtype)

        expected = ser_np.quantile(q=quantile, interpolation=interpolation)
        if quantile == 0.5:
            if pa_dtype.unit == "us":
                expected = expected.to_pydatetime(warn=False)
            assert result == expected
        else:
            if pa_dtype.unit == "us":
                expected = expected.dt.floor("us")
            tm.assert_series_equal(result, expected.astype(data.dtype))
        return

    if quantile == 0.5:
        assert result == data[0]
    else:
        # Just check the values
        expected = pd.Series(data.take([0, 0]), index=[0.5, 0.5])
        if (
            pa.types.is_integer(pa_dtype)
            or pa.types.is_floating(pa_dtype)
            or pa.types.is_decimal(pa_dtype)
        ):
            expected = expected.astype("float64[pyarrow]")
            result = result.astype("float64[pyarrow]")
        tm.assert_series_equal(result, expected)


def test_quantile(interpolation, a_vals, b_vals, q):
    all_vals = pd.concat([pd.Series(a_vals), pd.Series(b_vals)])

    a_expected = pd.Series(a_vals).quantile(q, interpolation=interpolation)
    b_expected = pd.Series(b_vals).quantile(q, interpolation=interpolation)

    df = DataFrame({"key": ["a"] * len(a_vals) + ["b"] * len(b_vals), "val": all_vals})

    expected = DataFrame(
        [a_expected, b_expected], columns=["val"], index=Index(["a", "b"], name="key")
    )
    if all_vals.dtype.kind == "M" and expected.dtypes.values[0].kind == "M":
        # TODO(non-nano): this should be unnecessary once array_to_datetime
        #  correctly infers non-nano from Timestamp.unit
        expected = expected.astype(all_vals.dtype)
    result = df.groupby("key").quantile(q, interpolation=interpolation)

    tm.assert_frame_equal(result, expected)

