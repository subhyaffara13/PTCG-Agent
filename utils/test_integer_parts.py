
def test_integer_parts():
    assert floor(3.2) == 3
    assert ceil(3.2) == 4
    assert floor(3.2+5j) == 3+5j
    assert ceil(3.2+5j) == 4+5j

