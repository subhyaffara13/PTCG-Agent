
def test_cmath_complex_identities():
    # Define symbol
    z = symbols('z')

    # Trigonometric identity using re(z) and im(z)
    expr = cos(z) - cos(re(z)) * cosh(im(z)) + I * sin(re(z)) * sinh(im(z))
    func = lambdify([z], expr, modules=["cmath", "math"])
    hpi = math.pi / 2
    assert abs(func(hpi + 1j * hpi)) < 4e-16

    # Euler's Formula: e^(i*z) = cos(z) + i*sin(z)
    func = lambdify([z], exp(I * z) - (cos(z) + I * sin(z)), modules=["cmath", "math"])
    assert abs(func(hpi)) < 4e-16

    # Exponential Identity: e^z = e^(Re(z)) * (cos(Im(z)) + i*sin(Im(z)))
    func_exp = lambdify([z], exp(z) - exp(re(z)) * (cos(im(z)) + I * sin(im(z))),
                        modules=["cmath", "math"])
    assert abs(func_exp(hpi + 1j * hpi)) < 4e-16

    # Complex Cosine Identity: cos(z) = cos(Re(z)) * cosh(Im(z)) - i*sin(Re(z)) * sinh(Im(z))
    func_cos = lambdify([z], cos(z) - (cos(re(z)) * cosh(im(z)) - I * sin(re(z)) * sinh(im(z))),
                        modules=["cmath", "math"])
    assert abs(func_cos(hpi + 1j * hpi)) < 4e-16

    # Complex Sine Identity: sin(z) = sin(Re(z)) * cosh(Im(z)) + i*cos(Re(z)) * sinh(Im(z))
    func_sin = lambdify([z], sin(z) - (sin(re(z)) * cosh(im(z)) + I * cos(re(z)) * sinh(im(z))),
                        modules=["cmath", "math"])
    assert abs(func_sin(hpi + 1j * hpi)) < 4e-16

    # Complex Hyperbolic Cosine Identity: cosh(z) = cosh(Re(z)) * cos(Im(z)) + i*sinh(Re(z)) * sin(Im(z))
    func_cosh_1 = lambdify([z], cosh(z) - (cosh(re(z)) * cos(im(z)) + I * sinh(re(z)) * sin(im(z))),
                         modules=["cmath", "math"])
    assert abs(func_cosh_1(hpi + 1j * hpi)) < 4e-16

    # Complex Hyperbolic Sine Identity: sinh(z) = sinh(Re(z)) * cos(Im(z)) + i*cosh(Re(z)) * sin(Im(z))
    func_sinh = lambdify([z], sinh(z) - (sinh(re(z)) * cos(im(z)) + I * cosh(re(z)) * sin(im(z))),
                         modules=["cmath", "math"])
    assert abs(func_sinh(hpi + 1j * hpi)) < 4e-16

    # cosh(z) = (e^z + e^(-z)) / 2
    func_cosh_2 = lambdify([z], cosh(z) - (exp(z) + exp(-z)) / 2, modules=["cmath", "math"])
    assert abs(func_cosh_2(hpi)) < 4e-16

    # Additional expressions testing log and exp with real and imaginary parts
    expr1 = log(re(z)) + log(im(z)) - log(re(z) * im(z))
    expr2 = exp(re(z)) * exp(im(z) * I) - exp(z)
    expr3 = log(exp(re(z))) - re(z)
    expr4 = exp(log(re(z))) - re(z)
    expr5 = log(exp(re(z) + im(z))) - (re(z) + im(z))
    expr6 = exp(log(re(z) + im(z))) - (re(z) + im(z))
    func1 = lambdify([z], expr1, modules=["cmath", "math"])
    func2 = lambdify([z], expr2, modules=["cmath", "math"])
    func3 = lambdify([z], expr3, modules=["cmath", "math"])
    func4 = lambdify([z], expr4, modules=["cmath", "math"])
    func5 = lambdify([z], expr5, modules=["cmath", "math"])
    func6 = lambdify([z], expr6, modules=["cmath", "math"])
    test_value = 3 + 4j
    assert abs(func1(test_value)) < 4e-16
    assert abs(func2(test_value)) < 4e-16
    assert abs(func3(test_value)) < 4e-16
    assert abs(func4(test_value)) < 4e-16
    assert abs(func5(test_value)) < 4e-16
    assert abs(func6(test_value)) < 4e-16

