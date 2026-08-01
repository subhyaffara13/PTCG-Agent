
def _higher_order_type2_to_sub_systems(J, f_t, funcs, t, max_order, b=None, P=None):

    # Note: To add a test for this ValueError
    if J is None or f_t is None or not _matrix_is_constant(J, t):
        raise ValueError(filldedent('''
            Correctly input for args 'A' and 'f_t' for Linear, Higher Order,
            Type 2
        '''))

    if P is None and b is not None and not b.is_zero_matrix:
        raise ValueError(filldedent('''
            Provide the keyword 'P' for matrix P in A = P * J * P-1.
        '''))

    new_funcs = Matrix([Function(Dummy('{}__0'.format(f.func.__name__)))(t) for f in funcs])
    new_eqs = new_funcs.diff(t, max_order) - f_t * J * new_funcs

    if b is not None and not b.is_zero_matrix:
        new_eqs -= P.inv() * b

    new_eqs = canonical_odes(new_eqs, new_funcs, t)[0]

    return new_eqs, new_funcs

