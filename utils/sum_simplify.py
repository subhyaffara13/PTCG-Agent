
def sum_simplify(s, **kwargs):
    """Main function for Sum simplification"""
    if not isinstance(s, Add):
        s = s.xreplace({a: sum_simplify(a, **kwargs)
            for a in s.atoms(Add) if a.has(Sum)})
    s = expand(s)
    if not isinstance(s, Add):
        return s

    terms = s.args
    s_t = [] # Sum Terms
    o_t = [] # Other Terms

    for term in terms:
        sum_terms, other = sift(Mul.make_args(term),
            lambda i: isinstance(i, Sum), binary=True)
        if not sum_terms:
            o_t.append(term)
            continue
        other = [Mul(*other)]
        s_t.append(Mul(*(other + [s._eval_simplify(**kwargs) for s in sum_terms])))

    result = Add(sum_combine(s_t), *o_t)

    return result

