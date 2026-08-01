
def test_complex_exponential():
    w = exp(-I*2*pi/3, evaluate=False)
    alg = QQ.algebraic_field(w)
    assert construct_domain([w**2, w, 1], extension=True) == (
        alg,
        [alg.convert(w**2),
         alg.convert(w),
         alg.convert(1)]
    )

