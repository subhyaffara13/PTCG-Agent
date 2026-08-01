
def test_replacer():
    if matchpy is None:
        skip("matchpy not installed")

    for info in [True, False]:
        for lambdify in [True, False]:
            _perform_test_replacer(info, lambdify)

