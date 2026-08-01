
def _cg_list(term):
    if isinstance(term, CG):
        return (term,), 1, 1
    cg = []
    coeff = 1
    if not isinstance(term, (Mul, Pow)):
        raise NotImplementedError('term must be CG, Add, Mul or Pow')
    if isinstance(term, Pow) and term.exp.is_number:
        if term.exp.is_number:
            [ cg.append(term.base) for _ in range(term.exp) ]
        else:
            return (term,), 1, 1
    if isinstance(term, Mul):
        for arg in term.args:
            if isinstance(arg, CG):
                cg.append(arg)
            else:
                coeff *= arg
        return cg, coeff, coeff/abs(coeff)

