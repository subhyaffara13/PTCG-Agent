
def test_pi_Pi():
    "Test that pi (instance) is imported, but Pi (class) is not"
    from sympy import pi  # noqa
    with raises(ImportError):
        from sympy import Pi  # noqa

