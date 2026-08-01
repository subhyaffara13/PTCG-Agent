
def test_logical(code, expected_number_of_lines):
    code = _generate(dedent(code))
    assert _logical(code) == expected_number_of_lines

