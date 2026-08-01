
def _select_equations(eqs, funcs, key=lambda x: x):
    eq_dict = {e.lhs: e.rhs for e in eqs}
    return [Eq(f, eq_dict[key(f)]) for f in funcs]

