
def test_wright_functional(a, b, x):
    """Test functional relation of wright_bessel.

    Phi(a, b-1, z) = a*z*Phi(a, b+a, z) + (b-1)*Phi(a, b, z)

    Note that d/dx Phi(a, b, x) = Phi(a, b-1, x)
    See Eq. (22) of
    B. Stankovic, On the Function of E. M. Wright,
    Publ. de l' Institut Mathematique, Beograd,
    Nouvelle S`er. 10 (1970), 113-124.
    """
    assert_allclose(wright_bessel(a, b - 1, x),
                    a * x * wright_bessel(a, b + a, x)
                    + (b - 1) * wright_bessel(a, b, x),
                    rtol=1e-8, atol=1e-8)

