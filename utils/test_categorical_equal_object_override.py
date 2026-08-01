
def test_categorical_equal_object_override(obj):
    data = [1, 2, 3, 4]
    msg = f"""{obj} are different

Attribute "ordered" are different
\\[left\\]:  False
\\[right\\]: True"""

    c1 = Categorical(data, ordered=False)
    c2 = Categorical(data, ordered=True)

    with pytest.raises(AssertionError, match=msg):
        tm.assert_categorical_equal(c1, c2, obj=obj)

