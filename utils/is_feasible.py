
def is_feasible(language, commands):
    # This test should always work, otherwise the compiler is not present.
    routine = make_routine("test", x)
    numerical_tests = [
        ("test", ( 1.0,), 1.0, 1e-15),
        ("test", (-1.0,), -1.0, 1e-15),
    ]
    try:
        run_test("is_feasible", [routine], numerical_tests, language, commands,
                 friendly=False)
        return True
    except AssertionError:
        return False

