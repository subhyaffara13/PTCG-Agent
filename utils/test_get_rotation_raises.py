
def test_get_rotation_raises():
    with pytest.raises(ValueError):
        Text(rotation='hozirontal')

