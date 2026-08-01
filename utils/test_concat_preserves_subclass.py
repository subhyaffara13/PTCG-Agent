
def test_concat_preserves_subclass(obj):
    # GH28330 -- preserve subclass

    result = concat([obj, obj])
    assert isinstance(result, type(obj))

