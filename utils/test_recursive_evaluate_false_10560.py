
def test_recursive_evaluate_false_10560():
    inputs = {
        '4*-3' : '4*-3',
        '-4*3' : '(-4)*3',
        "-2*x*y": '(-2)*x*y',
        "x*-4*x": "x*(-4)*x"
    }
    for text, result in inputs.items():
        assert parse_expr(text, evaluate=False) == parse_expr(result, evaluate=False)

