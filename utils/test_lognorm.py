
def test_lognorm():
    """
    Ref: https://math.montana.edu/jobo/st528/documents/relc.pdf

    The data is the locomotive control time to failure example that starts
    on page 8.  That's the 8th page in the PDF; the page number shown in
    the text is 270).
    The document includes SAS output for the data.
    """
    # These are the uncensored measurements.  There are also 59 right-censored
    # measurements where the lower bound is 135.
    miles_to_fail = [22.5, 37.5, 46.0, 48.5, 51.5, 53.0, 54.5, 57.5, 66.5,
                     68.0, 69.5, 76.5, 77.0, 78.5, 80.0, 81.5, 82.0, 83.0,
                     84.0, 91.5, 93.5, 102.5, 107.0, 108.5, 112.5, 113.5,
                     116.0, 117.0, 118.5, 119.0, 120.0, 122.5, 123.0, 127.5,
                     131.0, 132.5, 134.0]

    data = CensoredData.right_censored(miles_to_fail + [135]*59,
                                       [0]*len(miles_to_fail) + [1]*59)
    sigma, loc, scale = lognorm.fit(data, floc=0)

    assert loc == 0
    # Convert the lognorm parameters to the mu and sigma of the underlying
    # normal distribution.
    mu = np.log(scale)
    # The expected results are from the 17th page of the PDF document
    # (labeled page 279), in the SAS output on the right side of the page.
    assert_allclose(mu, 5.1169, rtol=5e-4)
    assert_allclose(sigma, 0.7055, rtol=5e-3)

