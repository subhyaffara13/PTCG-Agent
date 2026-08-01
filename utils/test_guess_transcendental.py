
def test_guess_transcendental():
    #transcendental functions
    assert guess_solve_strategy( exp(x) + 1, x )  # == GS_TRANSCENDENTAL
    assert guess_solve_strategy( 2*cos(x) - y, x )  # == GS_TRANSCENDENTAL
    assert guess_solve_strategy(
        exp(x) + exp(-x) - y, x )  # == GS_TRANSCENDENTAL
    assert guess_solve_strategy(3**x - 10, x)  # == GS_TRANSCENDENTAL
    assert guess_solve_strategy(-3**x + 10, x)  # == GS_TRANSCENDENTAL

    assert guess_solve_strategy(a*x**b - y, x)  # == GS_TRANSCENDENTAL

