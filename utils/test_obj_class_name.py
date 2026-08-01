
def test_obj_class_name():
    expected_name = "UserType" if env.PYPY else "pybind11_tests.UserType"
    assert m.obj_class_name(UserType(1)) == expected_name
    assert m.obj_class_name(UserType) == expected_name


def test_obj_class_name():
    assert m.obj_class_name(None) == "NoneType"
    assert m.obj_class_name(list) == "list"
    assert m.obj_class_name([]) == "list"

