
def test_deprecated_testing_randtest():
    with warns_deprecated_sympy():
        import sympy.testing.randtest  # noqa:F401

