
def test_issue_10773():
    inputs = {
    '-10/5': '(-10)/5',
    '-10/-5' : '(-10)/(-5)',
    }
    for text, result in inputs.items():
        assert parse_expr(text, evaluate=False) == parse_expr(result, evaluate=False)

