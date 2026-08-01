
def _inverse_mellin_transform(F, s, x_, strip, as_meijerg=False):
    """ A helper for the real inverse_mellin_transform function, this one here
        assumes x to be real and positive. """
    x = _dummy('t', 'inverse-mellin-transform', F, positive=True)
    # Actually, we won't try integration at all. Instead we use the definition
    # of the Meijer G function as a fairly general inverse mellin transform.
    F = F.rewrite(gamma)
    for g in [factor(F), expand_mul(F), expand(F)]:
        if g.is_Add:
            # do all terms separately
            ress = [_inverse_mellin_transform(G, s, x, strip, as_meijerg,
                                              noconds=False)
                    for G in g.args]
            conds = [p[1] for p in ress]
            ress = [p[0] for p in ress]
            res = Add(*ress)
            if not as_meijerg:
                res = factor(res, gens=res.atoms(Heaviside))
            return res.subs(x, x_), And(*conds)

        try:
            a, b, C, e, fac = _rewrite_gamma(g, s, strip[0], strip[1])
        except IntegralTransformError:
            continue
        try:
            G = meijerg(a, b, C/x**e)
        except ValueError:
            continue
        if as_meijerg:
            h = G
        else:
            try:
                from sympy.simplify import hyperexpand
                h = hyperexpand(G)
            except NotImplementedError:
                raise IntegralTransformError(
                    'Inverse Mellin', F, 'Could not calculate integral')

            if h.is_Piecewise and len(h.args) == 3:
                # XXX we break modularity here!
                h = Heaviside(x - Abs(C))*h.args[0].args[0] \
                    + Heaviside(Abs(C) - x)*h.args[1].args[0]
        # We must ensure that the integral along the line we want converges,
        # and return that value.
        # See [L], 5.2
        cond = [Abs(arg(G.argument)) < G.delta*pi]
        # Note: we allow ">=" here, this corresponds to convergence if we let
        # limits go to oo symmetrically. ">" corresponds to absolute convergence.
        cond += [And(Or(len(G.ap) != len(G.bq), 0 >= re(G.nu) + 1),
                     Abs(arg(G.argument)) == G.delta*pi)]
        cond = Or(*cond)
        if cond == False:
            raise IntegralTransformError(
                'Inverse Mellin', F, 'does not converge')
        return (h*fac).subs(x, x_), cond

    raise IntegralTransformError('Inverse Mellin', F, '')

