
def testcase(case):
    z, result = case
    print("Testing z =", z)
    mp.dps = 1010
    z = eval(z)
    mp.dps = maxdps + 50
    if result is None:
        gamma_val = gamma(z)
        loggamma_val = loggamma(z)
        factorial_val = factorial(z)
        rgamma_val = rgamma(z)
    else:
        loggamma_val = eval(result)
        gamma_val = exp(loggamma_val)
        factorial_val = z * gamma_val
        rgamma_val = 1/gamma_val
    for dps in [5, 10, 15, 25, 40, 60, 90, 120, 250, 600, 1000, 1800, 3600]:
        if dps > maxdps:
            break
        mp.dps = dps
        print("dps = %s" % dps)
        check("gamma", gamma, z, gamma_val)
        check("rgamma", rgamma, z, rgamma_val)
        check("loggamma", loggamma, z, loggamma_val)
        check("factorial", factorial, z, factorial_val)
        print()
        mp.dps = 15

