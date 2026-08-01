
def test_symbol_splitting():
    # By default Greek letter names should not be split (lambda is a keyword
    # so skip it)
    transformations = standard_transformations + (split_symbols,)
    greek_letters = ('alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta',
                     'eta', 'theta', 'iota', 'kappa', 'mu', 'nu', 'xi',
                     'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon',
                     'phi', 'chi', 'psi', 'omega')

    for letter in greek_letters:
        assert(parse_expr(letter, transformations=transformations) ==
               parse_expr(letter))

    # Make sure symbol splitting resolves names
    transformations += (implicit_multiplication,)
    local_dict = { 'e': sympy.E }
    cases = {
        'xe': 'E*x',
        'Iy': 'I*y',
        'ee': 'E*E',
    }
    for case, expected in cases.items():
        assert(parse_expr(case, local_dict=local_dict,
                          transformations=transformations) ==
               parse_expr(expected))

    # Make sure custom splitting works
    def can_split(symbol):
        if symbol not in ('unsplittable', 'names'):
            return _token_splittable(symbol)
        return False
    transformations = standard_transformations
    transformations += (split_symbols_custom(can_split),
                        implicit_multiplication)

    assert(parse_expr('unsplittable', transformations=transformations) ==
           parse_expr('unsplittable'))
    assert(parse_expr('names', transformations=transformations) ==
           parse_expr('names'))
    assert(parse_expr('xy', transformations=transformations) ==
           parse_expr('x*y'))
    for letter in greek_letters:
        assert(parse_expr(letter, transformations=transformations) ==
               parse_expr(letter))

