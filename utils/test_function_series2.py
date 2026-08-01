
def test_function_series2():
    """Create our new "cos" function."""

    for F in [Function, DefinedFunction]:

        class my_function2(F):

            def fdiff(self, argindex=1):
                return -sin(self.args[0])

            @classmethod
            def eval(cls, arg):
                arg = sympify(arg)
                if arg == 0:
                    return sympify(1)

        #Test that the taylor series is correct
        assert my_function2(x).series(x, 0, 10) == cos(x).series(x, 0, 10)

