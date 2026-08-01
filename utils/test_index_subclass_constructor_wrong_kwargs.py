
def test_index_subclass_constructor_wrong_kwargs(klass):
    # GH #19348
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        klass(foo="bar")

