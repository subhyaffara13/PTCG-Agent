
def test_visitor_containers(values, expected):
    expected_letter, expected_name, expected_str = expected

    cls = Function if len(values) == 8 else Class
    obj = cls(*values)
    assert obj.letter == expected_letter
    assert obj.fullname == expected_name
    assert str(obj) == expected_str

