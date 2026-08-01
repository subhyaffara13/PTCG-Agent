
def test_dtype_to_arrow_c_fmt_arrowdtype(pa_dtype, args_kwargs, c_string):
    # GH 52323
    pa = pytest.importorskip("pyarrow")
    if not args_kwargs:
        pa_type = getattr(pa, pa_dtype)()
    elif isinstance(args_kwargs, tuple):
        pa_type = getattr(pa, pa_dtype)(*args_kwargs)
    else:
        pa_type = getattr(pa, pa_dtype)(**args_kwargs)
    arrow_type = pd.ArrowDtype(pa_type)
    assert dtype_to_arrow_c_fmt(arrow_type) == c_string

