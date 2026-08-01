
def test_format_property():
    for fmt in sparray_types:
        arr_cls = getattr(scipy.sparse, f"{fmt}_array")
        M = arr_cls([[1, 2]])
        assert M.format == fmt
        assert M._format == fmt
        with pytest.raises(AttributeError):
            M.format = "qqq"

