
def test_special_values():
    # Test special values from Gauss's digamma theorem. See
    #
    # https://en.wikipedia.org/wiki/Digamma_function

    dataset = [
        (1, -euler),
        (0.5, -2*log(2) - euler),
        (1/3, -pi/(2*sqrt(3)) - 3*log(3)/2 - euler),
        (1/4, -pi/2 - 3*log(2) - euler),
        (1/6, -pi*sqrt(3)/2 - 2*log(2) - 3*log(3)/2 - euler),
        (1/8,
         -pi/2 - 4*log(2) - (pi + log(2 + sqrt(2)) - log(2 - sqrt(2)))/sqrt(2) - euler)
    ]

    dataset = np.asarray(dataset)
    FuncData(sc.digamma, dataset, 0, 1, rtol=1e-14).check()

