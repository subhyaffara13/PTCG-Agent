
def test_implicit_application():
    cases = {
        'factorial': 'factorial',
        'sin x': 'sin(x)',
        'tan y**3': 'tan(y**3)',
        'cos 2*x': 'cos(2*x)',
        '(cot)': 'cot',
        'sin cos tan x': 'sin(cos(tan(x)))'
    }
    transformations = standard_transformations + (convert_xor,)
    transformations2 = transformations + (implicit_application,)
    for case in cases:
        implicit = parse_expr(case, transformations=transformations2)
        normal = parse_expr(cases[case], transformations=transformations)
        assert(implicit == normal), (implicit, normal)

    multiplication = ['x y', 'x sin x', '2x']
    for case in multiplication:
        raises(SyntaxError,
               lambda: parse_expr(case, transformations=transformations2))
    raises(TypeError,
           lambda: parse_expr('sin**2(x)', transformations=transformations2))

