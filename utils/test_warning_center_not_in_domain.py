
def test_warning_center_not_in_domain():
    # UNURAN will warn if the center provided or the one computed w/o the
    # domain is outside of the domain
    msg = "102 : center moved into domain of distribution"
    with pytest.warns(RuntimeWarning, match=msg):
        NumericalInversePolynomial(StandardNormal(), center=0, domain=(3, 5))
    with pytest.warns(RuntimeWarning, match=msg):
        NumericalInversePolynomial(StandardNormal(), domain=(3, 5))

