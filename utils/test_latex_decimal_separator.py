
def test_latex_decimal_separator():

    x, y, z, t = symbols('x y z t')
    k, m, n = symbols('k m n', integer=True)
    f, g, h = symbols('f g h', cls=Function)

    # comma decimal_separator
    assert(latex([1, 2.3, 4.5], decimal_separator='comma') == r'\left[ 1; \  2{,}3; \  4{,}5\right]')
    assert(latex(FiniteSet(1, 2.3, 4.5), decimal_separator='comma') == r'\left\{1; 2{,}3; 4{,}5\right\}')
    assert(latex((1, 2.3, 4.6), decimal_separator = 'comma') == r'\left( 1; \  2{,}3; \  4{,}6\right)')
    assert(latex((1,), decimal_separator='comma') == r'\left( 1;\right)')

    # period decimal_separator
    assert(latex([1, 2.3, 4.5], decimal_separator='period') == r'\left[ 1, \  2.3, \  4.5\right]' )
    assert(latex(FiniteSet(1, 2.3, 4.5), decimal_separator='period') == r'\left\{1, 2.3, 4.5\right\}')
    assert(latex((1, 2.3, 4.6), decimal_separator = 'period') == r'\left( 1, \  2.3, \  4.6\right)')
    assert(latex((1,), decimal_separator='period') == r'\left( 1,\right)')

    # default decimal_separator
    assert(latex([1, 2.3, 4.5]) == r'\left[ 1, \  2.3, \  4.5\right]')
    assert(latex(FiniteSet(1, 2.3, 4.5)) == r'\left\{1, 2.3, 4.5\right\}')
    assert(latex((1, 2.3, 4.6)) == r'\left( 1, \  2.3, \  4.6\right)')
    assert(latex((1,)) == r'\left( 1,\right)')

    assert(latex(Mul(3.4,5.3), decimal_separator = 'comma') == r'18{,}02')
    assert(latex(3.4*5.3, decimal_separator = 'comma') == r'18{,}02')
    x = symbols('x')
    y = symbols('y')
    z = symbols('z')
    assert(latex(x*5.3 + 2**y**3.4 + 4.5 + z, decimal_separator = 'comma') == r'2^{y^{3{,}4}} + 5{,}3 x + z + 4{,}5')

    assert(latex(0.987, decimal_separator='comma') == r'0{,}987')
    assert(latex(S(0.987), decimal_separator='comma') == r'0{,}987')
    assert(latex(.3, decimal_separator='comma') == r'0{,}3')
    assert(latex(S(.3), decimal_separator='comma') == r'0{,}3')


    assert(latex(5.8*10**(-7), decimal_separator='comma') == r'5{,}8 \cdot 10^{-7}')
    assert(latex(S(5.7)*10**(-7), decimal_separator='comma') == r'5{,}7 \cdot 10^{-7}')
    assert(latex(S(5.7*10**(-7)), decimal_separator='comma') == r'5{,}7 \cdot 10^{-7}')

    x = symbols('x')
    assert(latex(1.2*x+3.4, decimal_separator='comma') == r'1{,}2 x + 3{,}4')
    assert(latex(FiniteSet(1, 2.3, 4.5), decimal_separator='period') == r'\left\{1, 2.3, 4.5\right\}')

    # Error Handling tests
    raises(ValueError, lambda: latex([1,2.3,4.5], decimal_separator='non_existing_decimal_separator_in_list'))
    raises(ValueError, lambda: latex(FiniteSet(1,2.3,4.5), decimal_separator='non_existing_decimal_separator_in_set'))
    raises(ValueError, lambda: latex((1,2.3,4.5), decimal_separator='non_existing_decimal_separator_in_tuple'))

