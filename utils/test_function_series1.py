
def test_function_series1():
    """Create our new "sin" function."""

    for F in [Function, DefinedFunction]:

        class my_function(F):

            def fdiff(self, argindex=1):
                return cos(self.args[0])

            @classmethod
            def eval(cls, arg):
                arg = sympify(arg)
                if arg == 0:
                    return sympify(0)

        #Test that the taylor series is correct
        assert my_function(x).series(x, 0, 10) == sin(x).series(x, 0, 10)
        assert limit(my_function(x)/x, x, 0) == 1

