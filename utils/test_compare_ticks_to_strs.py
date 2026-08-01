
def test_compare_ticks_to_strs(cls):
    # GH#23524
    off = cls(19)

    # These tests should work with any strings, but we particularly are
    #  interested in "infer" as that comparison is convenient to make in
    #  Datetime/Timedelta Array/Index constructors
    assert not off == "infer"
    assert not "foo" == off

    instance_type = ".".join([cls.__module__, cls.__name__])
    msg = (
        "'<'|'<='|'>'|'>=' not supported between instances of "
        f"'str' and '{instance_type}'|'{instance_type}' and 'str'"
    )

    for left, right in [("infer", off), (off, "infer")]:
        with pytest.raises(TypeError, match=msg):
            left < right
        with pytest.raises(TypeError, match=msg):
            left <= right
        with pytest.raises(TypeError, match=msg):
            left > right
        with pytest.raises(TypeError, match=msg):
            left >= right

