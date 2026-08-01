
def test_construct_from_string_raises():
    with pytest.raises(
        TypeError, match="Cannot construct a 'SparseDtype' from 'not a dtype'"
    ):
        SparseDtype.construct_from_string("not a dtype")

