
def test_info_memory_usage_deep_pypy():
    s_with_object_index = Series({"a": [1]}, index=["foo"])
    assert s_with_object_index.memory_usage(
        index=True, deep=True
    ) == s_with_object_index.memory_usage(index=True)

    s_object = Series({"a": ["a"]})
    assert s_object.memory_usage(deep=True) == s_object.memory_usage()


def test_info_memory_usage_deep_pypy():
    df_with_object_index = DataFrame({"a": [1]}, index=Index(["foo"], dtype=object))
    assert (
        df_with_object_index.memory_usage(index=True, deep=True).sum()
        == df_with_object_index.memory_usage(index=True).sum()
    )

    df_object = DataFrame({"a": Series(["a"], dtype=object)})
    assert df_object.memory_usage(deep=True).sum() == df_object.memory_usage().sum()

