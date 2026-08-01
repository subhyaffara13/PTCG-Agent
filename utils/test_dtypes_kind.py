
def test_dtypes_kind(kind):
    expected = dtype_categories[kind]
    if isinstance(expected, tuple):
        assert info.dtypes(kind=kind) == info.dtypes(kind=expected)
    else:
        assert info.dtypes(kind=kind) == expected

