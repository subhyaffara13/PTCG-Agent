
def _nonlin_line_search(func, x, Fx, dx, search_type='armijo', rdiff=1e-8,
                        smin=1e-2):
    tmp_s = [0]
    tmp_Fx = [Fx]
    tmp_phi = [norm(Fx)**2]
    s_norm = norm(x) / norm(dx)

    def phi(s, store=True):
        if s == tmp_s[0]:
            return tmp_phi[0]
        xt = x + s*dx
        v = func(xt)
        p = _safe_norm(v)**2
        if store:
            tmp_s[0] = s
            tmp_phi[0] = p
            tmp_Fx[0] = v
        return p

    def derphi(s):
        ds = (abs(s) + s_norm + 1) * rdiff
        return (phi(s+ds, store=False) - phi(s)) / ds

    if search_type == 'wolfe':
        s, phi1, phi0 = scalar_search_wolfe1(phi, derphi, tmp_phi[0],
                                             xtol=1e-2, amin=smin)
    elif search_type == 'armijo':
        s, phi1 = scalar_search_armijo(phi, tmp_phi[0], -tmp_phi[0],
                                       amin=smin)

    if s is None:
        # XXX: No suitable step length found. Take the full Newton step,
        #      and hope for the best.
        s = 1.0

    x = x + s*dx
    if s == tmp_s[0]:
        Fx = tmp_Fx[0]
    else:
        Fx = func(x)
    Fx_norm = norm(Fx)

    return s, x, Fx, Fx_norm

