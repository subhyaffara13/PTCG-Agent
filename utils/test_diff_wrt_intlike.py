
def test_diff_wrt_intlike():
    class Two:
        def __int__(self):
            return 2

    assert cos(x).diff(x, Two()) == -cos(x)

