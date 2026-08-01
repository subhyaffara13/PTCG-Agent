
def test_subs_wild():
    R, S, T, U = symbols('R S T U', cls=Wild)

    assert (R*S).subs(R*S, T) == T
    assert (S*R).subs(R*S, T) == T
    assert (R + S).subs(R + S, T) == T
    assert (R**S).subs(R, T) == T**S
    assert (R**S).subs(S, T) == R**T
    assert (R*S**T).subs(R, U) == U*S**T
    assert (R*S**T).subs(S, U) == R*U**T
    assert (R*S**T).subs(T, U) == R*S**U

