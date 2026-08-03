from typing import Tuple

def can_do(ap, bq, numerical=True, div=1, lowerplane=False):
    r = hyperexpand(hyper(ap, bq, z))
    if r.has(hyper):
        return False
    if not numerical:
        return True
    repl = {}
    randsyms = r.free_symbols - {z}
    while randsyms:
        # Only randomly generated parameters are checked.
        for n, ai in enumerate(randsyms):
            repl[ai] = randcplx(n)/div
        if not any(b.is_Integer and b <= 0 for b in Tuple(*bq).subs(repl)):
            break
    [a, b, c, d] = [2, -1, 3, 1]
    if lowerplane:
        [a, b, c, d] = [2, -2, 3, -1]
    return tn(
        hyper(ap, bq, z).subs(repl),
        r.replace(exp_polar, exp).subs(repl),
        z, a=a, b=b, c=c, d=d)

