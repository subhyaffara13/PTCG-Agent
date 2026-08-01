
def test_string_delimiter(styler):
    result = styler.to_string(delimiter=";")
    expected = dedent(
        """\
    ;A;B;C
    0;0;-0.61;ab
    1;1;-1.22;cd
    """
    )
    assert result == expected

