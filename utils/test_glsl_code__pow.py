
def test_glsl_code_Pow():
    g = implemented_function('g', Lambda(x, 2*x))
    assert glsl_code(x**3) == "pow(x, 3.0)"
    assert glsl_code(x**(y**3)) == "pow(x, pow(y, 3.0))"
    assert glsl_code(1/(g(x)*3.5)**(x - y**x)/(x**2 + y)) == \
        "pow(3.5*2*x, -x + pow(y, x))/(pow(x, 2.0) + y)"
    assert glsl_code(x**-1.0) == '1.0/x'

