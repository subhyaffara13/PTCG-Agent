
def test_custom_function_precedence_comparison():
    """
    Test cases for custom functions with different precedence values,
    specifically handling:
    1. Functions with precedence < PRECEDENCE["Mul"] (50)
    2. Functions with precedence = Func (70)

    Key distinction:
    1. Lower precedence functions (45) need parentheses: -2*(x F y)
    2. Higher precedence functions (70) don't: -2*x F y
    """
    class LowPrecedenceF(Function):
        precedence = PRECEDENCE["Mul"] - 5
        def _sympystr(self, printer):
            return f"{printer._print(self.args[0])} F {printer._print(self.args[1])}"

    class HighPrecedenceF(Function):
        precedence = PRECEDENCE["Func"]
        def _sympystr(self, printer):
            return f"{printer._print(self.args[0])} F {printer._print(self.args[1])}"

    def test_low_precedence():
        expr1 = 2 * LowPrecedenceF(x, y)
        assert str(expr1) == "2*(x F y)"

        expr2 = -2 * LowPrecedenceF(x, y)
        assert str(expr2) == "-2*(x F y)"

    def test_high_precedence():
        expr1 = 2 * HighPrecedenceF(x, y)
        assert str(expr1) == "2*x F y"

        expr2 = -2 * HighPrecedenceF(x, y)
        assert str(expr2) == "-2*x F y"

    test_low_precedence()
    test_high_precedence()

