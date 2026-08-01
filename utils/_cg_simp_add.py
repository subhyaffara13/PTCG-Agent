
def _cg_simp_add(e):
    #TODO: Improve simplification method
    """Takes a sum of terms involving Clebsch-Gordan coefficients and
    simplifies the terms.

    Explanation
    ===========

    First, we create two lists, cg_part, which is all the terms involving CG
    coefficients, and other_part, which is all other terms. The cg_part list
    is then passed to the simplification methods, which return the new cg_part
    and any additional terms that are added to other_part
    """
    cg_part = []
    other_part = []

    e = expand(e)
    for arg in e.args:
        if arg.has(CG):
            if isinstance(arg, Sum):
                other_part.append(_cg_simp_sum(arg))
            elif isinstance(arg, Mul):
                terms = 1
                for term in arg.args:
                    if isinstance(term, Sum):
                        terms *= _cg_simp_sum(term)
                    else:
                        terms *= term
                if terms.has(CG):
                    cg_part.append(terms)
                else:
                    other_part.append(terms)
            else:
                cg_part.append(arg)
        else:
            other_part.append(arg)

    cg_part, other = _check_varsh_871_1(cg_part)
    other_part.append(other)
    cg_part, other = _check_varsh_871_2(cg_part)
    other_part.append(other)
    cg_part, other = _check_varsh_872_9(cg_part)
    other_part.append(other)
    return Add(*cg_part) + Add(*other_part)

