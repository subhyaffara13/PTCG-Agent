
def test_weights_integer():
    # integer weights are OK, cf gh-9709 (comment)
    values = [0.2, 13.5, 21.0, 75.0, 99.0]
    weights = [1, 2, 4, 8, 16]  # a list of integers
    pdf_i = stats.gaussian_kde(values, weights=weights)
    pdf_f = stats.gaussian_kde(values, weights=np.float64(weights))

    xn = [0.3, 11, 88]
    assert_allclose(pdf_i.evaluate(xn),
                    pdf_f.evaluate(xn), atol=1e-14, rtol=1e-14)

