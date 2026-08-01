
def test_printmethod():
    class fabs(Abs):
        def _ccode(self, printer):
            return "fabs(%s)" % printer._print(self.args[0])

    assert ccode(fabs(x)) == "fabs(x)"


def test_printmethod():
    x = symbols('x')

    class nint(Function):
        def _fcode(self, printer):
            return "nint(%s)" % printer._print(self.args[0])
    assert fcode(nint(x)) == "      nint(x)"


def test_printmethod():
    assert glsl_code(Abs(x)) == "abs(x)"


def test_printmethod():
    assert jscode(Abs(x)) == "Math.abs(x)"


def test_printmethod():
    # In each case, printmethod is called to test
    # its working

    obj = CustomPrintedObject()
    assert LambdaPrinter().doprint(obj) == 'lambda'
    assert TensorflowPrinter().doprint(obj) == 'tensorflow'
    assert NumExprPrinter().doprint(obj) == "numexpr.evaluate('numexpr', truediv=True)"

    assert NumExprPrinter().doprint(Piecewise((y, x >= 0), (z, x < 0))) == \
            "numexpr.evaluate('where((x >= 0), y, z)', truediv=True)"


def test_printmethod():
    class R(Abs):
        def _latex(self, printer):
            return "foo(%s)" % printer._print(self.args[0])
    assert latex(R(x)) == r"foo(x)"

    class R(Abs):
        def _latex(self, printer):
            return "foo"
    assert latex(R(x)) == r"foo"


def test_printmethod():
    obj = CustomPrintedObject()
    assert NumPyPrinter().doprint(obj) == 'numpy'
    assert MpmathPrinter().doprint(obj) == 'mpmath'


def test_printmethod():
    class fabs(Abs):
        def _rcode(self, printer):
            return "abs(%s)" % printer._print(self.args[0])

    assert rcode(fabs(x)) == "abs(x)"


def test_printmethod():
    class R(Abs):
        def _sympyrepr(self, printer):
            return "foo(%s)" % printer._print(self.args[0])
    assert srepr(R(x)) == "foo(Symbol('x'))"


def test_printmethod():
    class fabs(Abs):
        def _rust_code(self, printer):
            return "%s.fabs()" % printer._print(self.args[0])
    assert rust_code(fabs(x)) == "x.fabs()"
    a = MatrixSymbol("a", 1, 3)
    assert rust_code(a[0,0]) == 'a[0]'


def test_printmethod():
    class R(Abs):
        def _sympystr(self, printer):
            return "foo(%s)" % printer._print(self.args[0])
    assert sstr(R(x)) == "foo(x)"

    class R(Abs):
        def _sympystr(self, printer):
            return "foo"
    assert sstr(R(x)) == "foo"

