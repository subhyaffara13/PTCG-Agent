
def _is_sum_surds(p):
    return all(f.is_Rational or f.is_Pow and
        f.base.is_Rational and (2*f.exp).is_Integer and f.is_extended_real
        for t in Add.make_args(p) for f in Mul.make_args(t))

