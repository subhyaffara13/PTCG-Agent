
def test_ccode_array_like_containers():
    assert ccode([2,3,4]) == "{2, 3, 4}"
    assert ccode((2,3,4)) == "{2, 3, 4}"

