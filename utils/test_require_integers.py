
def test_require_integers(offset_types):
    cls = offset_types
    with pytest.raises(ValueError, match="argument must be an integer"):
        cls(n=1.5)

