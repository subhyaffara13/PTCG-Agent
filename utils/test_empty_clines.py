
def test_empty_clines(columns, expected: str, clines: str):
    # GH 47203
    df = DataFrame(columns=columns)
    result = df.style.to_latex(clines=clines)
    assert result == expected

