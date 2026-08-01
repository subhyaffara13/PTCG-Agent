
def test_set_wrong_linestyle():
    c = Collection()
    with pytest.raises(ValueError, match="Do not know how to convert 'fuzzy'"):
        c.set_linestyle('fuzzy')

