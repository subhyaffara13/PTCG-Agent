
def test_lamda():
    assert latex(Symbol('lamda')) == r"\lambda"
    assert latex(Symbol('Lamda')) == r"\Lambda"

