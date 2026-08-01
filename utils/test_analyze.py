
def test_analyze(code, expected):
    code = dedent(code)

    try:
        len(expected)
    except:
        with pytest.raises(expected):
            analyze(code)
    else:
        result = analyze(code)
        assert result == Module(*expected)
        assert (
            result.loc
            == result.blank
            + result.sloc
            + result.single_comments
            + result.multi
        )

