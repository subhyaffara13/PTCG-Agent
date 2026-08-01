
def test_issue_gh_16734():
    # https://github.com/sympy/sympy/issues/16734

    syms = list(symbols('x, y'))

    def thread1():
        for n in range(1000):
            syms[0], syms[1] = symbols(f'x{n}, y{n}')
            syms[0].is_positive # Check an assumption in this thread.
        syms[0] = None

    def thread2():
        while syms[0] is not None:
            # Compare the symbol in this thread.
            result = (syms[0] == syms[1])  # noqa

    # Previously this would be very likely to raise an exception:
    thread = threading.Thread(target=thread1)
    thread.start()
    thread2()
    thread.join()

