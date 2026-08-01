
def test_is_function_class_equation():
    assert _is_function_class_equation(TrigonometricFunction,
                                       tan(x), x) is True
    assert _is_function_class_equation(TrigonometricFunction,
                                       tan(x) - 1, x) is True
    assert _is_function_class_equation(TrigonometricFunction,
                                       tan(x) + sin(x), x) is True
    assert _is_function_class_equation(TrigonometricFunction,
                                       tan(x) + sin(x) - a, x) is True
    assert _is_function_class_equation(TrigonometricFunction,
                                       sin(x)*tan(x) + sin(x), x) is True
    assert _is_function_class_equation(TrigonometricFunction,
                                       sin(x)*tan(x + a) + sin(x), x) is True
    assert _is_function_class_equation(TrigonometricFunction,
                                       sin(x)*tan(x*a) + sin(x), x) is True
    assert _is_function_class_equation(TrigonometricFunction,
                                       a*tan(x) - 1, x) is True
    assert _is_function_class_equation(TrigonometricFunction,
                                       tan(x)**2 + sin(x) - 1, x) is True
    assert _is_function_class_equation(TrigonometricFunction,
                                       tan(x) + x, x) is False
    assert _is_function_class_equation(TrigonometricFunction,
                                       tan(x**2), x) is False
    assert _is_function_class_equation(TrigonometricFunction,
                                       tan(x**2) + sin(x), x) is False
    assert _is_function_class_equation(TrigonometricFunction,
                                       tan(x)**sin(x), x) is False
    assert _is_function_class_equation(TrigonometricFunction,
                                       tan(sin(x)) + sin(x), x) is False
    assert _is_function_class_equation(HyperbolicFunction,
                                       tanh(x), x) is True
    assert _is_function_class_equation(HyperbolicFunction,
                                       tanh(x) - 1, x) is True
    assert _is_function_class_equation(HyperbolicFunction,
                                       tanh(x) + sinh(x), x) is True
    assert _is_function_class_equation(HyperbolicFunction,
                                       tanh(x) + sinh(x) - a, x) is True
    assert _is_function_class_equation(HyperbolicFunction,
                                       sinh(x)*tanh(x) + sinh(x), x) is True
    assert _is_function_class_equation(HyperbolicFunction,
                                       sinh(x)*tanh(x + a) + sinh(x), x) is True
    assert _is_function_class_equation(HyperbolicFunction,
                                       sinh(x)*tanh(x*a) + sinh(x), x) is True
    assert _is_function_class_equation(HyperbolicFunction,
                                       a*tanh(x) - 1, x) is True
    assert _is_function_class_equation(HyperbolicFunction,
                                       tanh(x)**2 + sinh(x) - 1, x) is True
    assert _is_function_class_equation(HyperbolicFunction,
                                       tanh(x) + x, x) is False
    assert _is_function_class_equation(HyperbolicFunction,
                                       tanh(x**2), x) is False
    assert _is_function_class_equation(HyperbolicFunction,
                                       tanh(x**2) + sinh(x), x) is False
    assert _is_function_class_equation(HyperbolicFunction,
                                       tanh(x)**sinh(x), x) is False
    assert _is_function_class_equation(HyperbolicFunction,
                                       tanh(sinh(x)) + sinh(x), x) is False

