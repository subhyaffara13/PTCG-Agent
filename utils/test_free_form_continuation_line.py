
def test_free_form_continuation_line():
    x, y = symbols('x,y')
    result = fcode(((cos(x) + sin(y))**(7)).expand(), source_format='free')
    expected = (
        'sin(y)**7 + 7*sin(y)**6*cos(x) + 21*sin(y)**5*cos(x)**2 + 35*sin(y)**4* &\n'
        '      cos(x)**3 + 35*sin(y)**3*cos(x)**4 + 21*sin(y)**2*cos(x)**5 + 7* &\n'
        '      sin(y)*cos(x)**6 + cos(x)**7'
    )
    assert result == expected

