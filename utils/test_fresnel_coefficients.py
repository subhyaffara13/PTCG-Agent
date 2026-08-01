
def test_fresnel_coefficients():
    assert all(ae(i, j, 5) for i, j in zip(
        fresnel_coefficients(0.5, 1, 1.33),
        [0.11163, -0.17138, 0.83581, 0.82862]))
    assert all(ae(i, j, 5) for i, j in zip(
        fresnel_coefficients(0.5, 1.33, 1),
        [-0.07726, 0.20482, 1.22724, 1.20482]))
    m1 = Medium('m1')
    m2 = Medium('m2', n=2)
    assert all(ae(i, j, 5) for i, j in zip(
        fresnel_coefficients(0.3, m1, m2),
        [0.31784, -0.34865, 0.65892, 0.65135]))
    ans = [[-0.23563, -0.97184], [0.81648, -0.57738]]
    got = fresnel_coefficients(0.6, m2, m1)
    for i, j in zip(got, ans):
        for a, b in zip(i.as_real_imag(), j):
            assert ae(a, b, 5)

