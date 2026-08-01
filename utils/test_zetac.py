
def test_zetac():
    # Expected values in the following were computed using Wolfram
    # Alpha's `Zeta[x] - 1`
    x = [-2.1, 0.8, 0.9999, 9, 50, 75]
    desired = [
        -0.9972705002153750,
        -5.437538415895550,
        -10000.42279161673,
        0.002008392826082214,
        8.881784210930816e-16,
        2.646977960169853e-23,
    ]
    assert_allclose(sc.zetac(x), desired, rtol=1e-12)

