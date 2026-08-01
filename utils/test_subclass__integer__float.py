
def test_subclass_Integer_Float():
    class MyPrinter(CXX17CodePrinter):
        def _print_Integer(self, arg):
            return 'bigInt("%s")' % super()._print_Integer(arg)

        def _print_Float(self, arg):
            rat = Rational(arg)
            return 'bigFloat(%s, %s)' % (
                self._print(Integer(rat.p)),
                self._print(Integer(rat.q))
            )

    p = MyPrinter()
    for i in range(13):
        assert p.doprint(i) == 'bigInt("%d")' % i
    assert p.doprint(Float(0.5)) == 'bigFloat(bigInt("1"), bigInt("2"))'
    assert p.doprint(x**-1.0) == 'bigFloat(bigInt("1"), bigInt("1"))/x'

