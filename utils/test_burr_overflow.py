
def test_burr_overflow():
    # this case leads to an overflow error if math.exp is used
    # in the definition of the burr pdf instead of np.exp
    # a direct implementation of the PDF as x**(-c-1) / (1+x**(-c))**(d+1)
    # also leads to an overflow error in the setup
    args = (1.89128135, 0.30195177)
    with warnings.catch_warnings():
        # filter potential overflow warning
        warnings.simplefilter("ignore", RuntimeWarning)
        gen = FastGeneratorInversion(stats.burr(*args))
    u_error, _ = gen.evaluate_error(random_state=4326)
    assert u_error <= 1e-10

