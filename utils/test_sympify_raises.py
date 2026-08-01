
def test_sympify_raises():
    raises(SympifyError, lambda: sympify("fx)"))

    class A:
        def __str__(self):
            return 'x'

    raises(SympifyError, lambda: sympify(A()))

