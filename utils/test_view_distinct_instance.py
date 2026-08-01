
def test_view_distinct_instance():
    a = np.array(["a" * 20, "b" * 20], dtype="T")

    assert_array_equal(a.view(a.dtype), a)

    # a view through any other instance would attach an unrelated allocator,
    # which the generalized reference-safety check rejects
    with pytest.raises(TypeError, match="Cannot change data-type"):
        a.view(StringDType())
    with pytest.raises(TypeError, match="Cannot get/set field"):
        a.getfield(StringDType())
    with pytest.raises(TypeError, match="Cannot change data-type"):
        with pytest.warns(DeprecationWarning, match="Setting the dtype"):
            a.dtype = StringDType()

    res = a.astype(StringDType())
    assert res.dtype is not a.dtype
    assert_array_equal(res, a)

