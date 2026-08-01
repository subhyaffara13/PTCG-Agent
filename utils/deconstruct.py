
def deconstruct(s, variables=()):
    """ Turn a SymPy object into a Compound """
    if s in variables:
        return Variable(s)
    if isinstance(s, (Variable, CondVariable)):
        return s
    if not isinstance(s, Basic) or s.is_Atom:
        return s
    return Compound(s.__class__,
                    tuple(deconstruct(arg, variables) for arg in s.args))

