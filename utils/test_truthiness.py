
def test_truthiness():
    msg = "boolean value of NA is ambiguous"

    with pytest.raises(TypeError, match=msg):
        bool(NA)

    with pytest.raises(TypeError, match=msg):
        not NA


def test_truthiness(value, expected):
    # https://github.com/pandas-dev/pandas/issues/21484
    assert bool(value) is expected

