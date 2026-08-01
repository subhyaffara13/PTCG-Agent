
def test_non_converting_constructors():
    non_converting_test_cases = [
        ("bytes", range(10)),
        ("none", 42),
        ("ellipsis", 42),
        ("type", 42),
    ]
    for t, v in non_converting_test_cases:
        for move in [True, False]:
            with pytest.raises(TypeError) as excinfo:
                m.nonconverting_constructor(t, v, move)
            expected_error = (
                f"Object of type '{type(v).__name__}' is not an instance of '{t}'"
            )
            assert str(excinfo.value) == expected_error

