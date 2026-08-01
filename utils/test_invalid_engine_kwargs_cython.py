
def test_invalid_engine_kwargs_cython():
    with pytest.raises(ValueError, match="cython engine does not accept engine_kwargs"):
        Series(range(1)).rolling(1).apply(
            lambda x: x, engine="cython", engine_kwargs={"nopython": False}
        )

