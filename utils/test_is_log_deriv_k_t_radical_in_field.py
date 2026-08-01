
def test_is_log_deriv_k_t_radical_in_field():
    # NOTE: any potential constant factor in the second element of the result
    # doesn't matter, because it cancels in Da/a.
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1/x, t)]})
    assert is_log_deriv_k_t_radical_in_field(Poly(5*t + 1, t), Poly(2*t*x, t), DE) == \
        (2, t*x**5)
    assert is_log_deriv_k_t_radical_in_field(Poly(2 + 3*t, t), Poly(5*x*t, t), DE) == \
        (5, x**3*t**2)

    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(-t/x**2, t)]})
    assert is_log_deriv_k_t_radical_in_field(Poly(-(1 + 2*t), t),
    Poly(2*x**2 + 2*x**2*t, t), DE) == \
        (2, t + t**2)
    assert is_log_deriv_k_t_radical_in_field(Poly(-1, t), Poly(x**2, t), DE) == \
        (1, t)
    assert is_log_deriv_k_t_radical_in_field(Poly(1, t), Poly(2*x**2, t), DE) == \
        (2, 1/t)

