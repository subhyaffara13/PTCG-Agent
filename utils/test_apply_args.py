
def test_apply_args(float_frame, axis, raw, engine, nopython):
    numba = pytest.importorskip("numba")
    if (
        engine == "numba"
        and Version(numba.__version__) == Version("0.61")
        and is_platform_arm()
    ):
        pytest.skip(f"Segfaults on ARM platforms with numba {numba.__version__}")
    engine_kwargs = {"nopython": nopython}
    result = float_frame.apply(
        lambda x, y: x + y,
        axis,
        args=(1,),
        raw=raw,
        engine=engine,
        engine_kwargs=engine_kwargs,
    )
    expected = float_frame + 1
    tm.assert_frame_equal(result, expected)

    # GH:58712
    result = float_frame.apply(
        lambda x, a, b: x + a + b,
        args=(1,),
        b=2,
        raw=raw,
        engine=engine,
        engine_kwargs=engine_kwargs,
    )
    expected = float_frame + 3
    tm.assert_frame_equal(result, expected)

    if engine == "numba":
        # py signature binding
        with pytest.raises(TypeError, match="missing a required argument: 'a'"):
            float_frame.apply(
                lambda x, a: x + a,
                b=2,
                raw=raw,
                engine=engine,
                engine_kwargs=engine_kwargs,
            )

        # keyword-only arguments are not supported in numba
        with pytest.raises(
            pd.errors.NumbaUtilError,
            match="numba does not support keyword-only arguments",
        ):
            float_frame.apply(
                lambda x, a, *, b: x + a + b,
                args=(1,),
                b=2,
                raw=raw,
                engine=engine,
                engine_kwargs=engine_kwargs,
            )

        with pytest.raises(
            pd.errors.NumbaUtilError,
            match="numba does not support keyword-only arguments",
        ):
            float_frame.apply(
                lambda *x, b: x[0] + x[1] + b,
                args=(1,),
                b=2,
                raw=raw,
                engine=engine,
                engine_kwargs=engine_kwargs,
            )


def test_apply_args():
    s = Series(["foo,bar"])

    result = s.apply(str.split, args=(",",))
    assert result[0] == ["foo", "bar"]
    assert isinstance(result[0], list)

