
def test_convert_to_tuples_of_quantities():
    from sympy.core.symbol import symbols

    alpha, beta = symbols('alpha beta')

    assert convert_to(speed_of_light, [meter, second]) == 299792458 * meter / second
    assert convert_to(speed_of_light, (meter, second)) == 299792458 * meter / second
    assert convert_to(speed_of_light, Tuple(meter, second)) == 299792458 * meter / second
    assert convert_to(joule, [meter, kilogram, second]) == kilogram*meter**2/second**2
    assert convert_to(joule, [centimeter, gram, second]) == 10000000*centimeter**2*gram/second**2
    assert convert_to(299792458*meter/second, [speed_of_light]) == speed_of_light
    assert convert_to(speed_of_light / 2, [meter, second, kilogram]) == meter/second*299792458 / 2
    # This doesn't make physically sense, but let's keep it as a conversion test:
    assert convert_to(2 * speed_of_light, [meter, second, kilogram]) == 2 * 299792458 * meter / second
    assert convert_to(G, [G, speed_of_light, planck]) == 1.0*G

    assert NS(convert_to(meter, [G, speed_of_light, hbar]), n=7) == '6.187142e+34*gravitational_constant**0.5000000*hbar**0.5000000/speed_of_light**1.500000'
    assert NS(convert_to(planck_mass, kilogram), n=7) == '2.176434e-8*kilogram'
    assert NS(convert_to(planck_length, meter), n=7) == '1.616255e-35*meter'
    assert NS(convert_to(planck_time, second), n=6) == '5.39125e-44*second'
    assert NS(convert_to(planck_temperature, kelvin), n=7) == '1.416784e+32*kelvin'
    assert NS(convert_to(convert_to(meter, [G, speed_of_light, planck]), meter), n=10) == '1.000000000*meter'

    # similar to https://github.com/sympy/sympy/issues/26263
    assert convert_to(sqrt(meter**2 + second**2.0), [meter, second]) == sqrt(meter**2 + second**2.0)
    assert convert_to((meter**2 + second**2.0)**2, [meter, second]) == (meter**2 + second**2.0)**2

    # similar to https://github.com/sympy/sympy/issues/21463
    assert convert_to(1/(beta*meter + meter), 1/meter) == 1/(beta*meter + meter)
    assert convert_to(1/(beta*meter + alpha*meter), 1/kilometer) == (1/(kilometer*beta/1000 + alpha*kilometer/1000))

