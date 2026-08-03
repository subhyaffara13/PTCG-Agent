import re

def _laplace_trig_ltex(xm, t, s):
    """
    Helper function for `_laplace_rule_trig`.  This function takes the list of
    exponentials `xm` from `_laplace_trig_expsum` and simplifies complex
    conjugate and real symmetric poles.  It returns the result as a sum and
    the convergence plane.
    """
    results = []
    planes = []

    def _simpc(coeffs):
        nc = coeffs.copy()
        for k in range(len(nc)):
            ri = nc[k].as_real_imag()
            if ri[0].has(im):
                nc[k] = nc[k].rewrite(cos)
            else:
                nc[k] = (ri[0] + I*ri[1]).rewrite(cos)
        return nc

    def _quadpole(t1, k1, k2, k3, s):
        a, k0, a_r, a_i = t1['a'], t1['k'], t1[re], t1[im]
        nc = [
            k0 + k1 + k2 + k3,
            a*(k0 + k1 - k2 - k3) - 2*I*a_i*k1 + 2*I*a_i*k2,
            (
                a**2*(-k0 - k1 - k2 - k3) +
                a*(4*I*a_i*k0 + 4*I*a_i*k3) +
                4*a_i**2*k0 + 4*a_i**2*k3),
            (
                a**3*(-k0 - k1 + k2 + k3) +
                a**2*(4*I*a_i*k0 + 2*I*a_i*k1 - 2*I*a_i*k2 - 4*I*a_i*k3) +
                a*(4*a_i**2*k0 - 4*a_i**2*k3))
        ]
        dc = [
            S.One, S.Zero, 2*a_i**2 - 2*a_r**2,
            S.Zero, a_i**4 + 2*a_i**2*a_r**2 + a_r**4]
        n = Add(
            *[x*s**y for x, y in zip(_simpc(nc), range(len(nc))[::-1])])
        d = Add(
            *[x*s**y for x, y in zip(dc, range(len(dc))[::-1])])
        return n/d

    def _ccpole(t1, k1, s):
        a, k0, a_r, a_i = t1['a'], t1['k'], t1[re], t1[im]
        nc = [k0 + k1, -a*k0 - a*k1 + 2*I*a_i*k0]
        dc = [S.One, -2*a_r, a_i**2 + a_r**2]
        n = Add(
            *[x*s**y for x, y in zip(_simpc(nc), range(len(nc))[::-1])])
        d = Add(
            *[x*s**y for x, y in zip(dc, range(len(dc))[::-1])])
        return n/d

    def _rspole(t1, k2, s):
        a, k0, a_r, a_i = t1['a'], t1['k'], t1[re], t1[im]
        nc = [k0 + k2, a*k0 - a*k2 - 2*I*a_i*k0]
        dc = [S.One, -2*I*a_i, -a_i**2 - a_r**2]
        n = Add(
            *[x*s**y for x, y in zip(_simpc(nc), range(len(nc))[::-1])])
        d = Add(
            *[x*s**y for x, y in zip(dc, range(len(dc))[::-1])])
        return n/d

    def _sypole(t1, k3, s):
        a, k0 = t1['a'], t1['k']
        nc = [k0 + k3, a*(k0 - k3)]
        dc = [S.One, S.Zero, -a**2]
        n = Add(
            *[x*s**y for x, y in zip(_simpc(nc), range(len(nc))[::-1])])
        d = Add(
            *[x*s**y for x, y in zip(dc, range(len(dc))[::-1])])
        return n/d

    def _simplepole(t1, s):
        a, k0 = t1['a'], t1['k']
        n = k0
        d = s - a
        return n/d

    while len(xm) > 0:
        t1 = xm.pop()
        i_imagsym = None
        i_realsym = None
        i_pointsym = None
        # The following code checks all remaining poles. If t1 is a pole at
        # a+b*I, then we check for a-b*I, -a+b*I, and -a-b*I, and
        # assign the respective indices to i_imagsym, i_realsym, i_pointsym.
        # -a-b*I / i_pointsym only applies if both a and b are != 0.
        for i in range(len(xm)):
            real_eq = t1[re] == xm[i][re]
            realsym = t1[re] == -xm[i][re]
            imag_eq = t1[im] == xm[i][im]
            imagsym = t1[im] == -xm[i][im]
            if realsym and imagsym and t1[re] != 0 and t1[im] != 0:
                i_pointsym = i
            elif realsym and imag_eq and t1[re] != 0:
                i_realsym = i
            elif real_eq and imagsym and t1[im] != 0:
                i_imagsym = i

        # The next part looks for four possible pole constellations:
        # quad:   a+b*I, a-b*I, -a+b*I, -a-b*I
        # cc:     a+b*I, a-b*I (a may be zero)
        # quad:   a+b*I, -a+b*I (b may be zero)
        # point:  a+b*I, -a-b*I (a!=0 and b!=0 is needed, but that has been
        #                        asserted when finding i_pointsym above.)
        # If none apply, then t1 is a simple pole.
        if (
                i_imagsym is not None and i_realsym is not None
                and i_pointsym is not None):
            results.append(
                _quadpole(t1,
                          xm[i_imagsym]['k'], xm[i_realsym]['k'],
                          xm[i_pointsym]['k'], s))
            planes.append(Abs(re(t1['a'])))
            # The three additional poles have now been used; to pop them
            # easily we have to do it from the back.
            indices_to_pop = [i_imagsym, i_realsym, i_pointsym]
            indices_to_pop.sort(reverse=True)
            for i in indices_to_pop:
                xm.pop(i)
        elif i_imagsym is not None:
            results.append(_ccpole(t1, xm[i_imagsym]['k'], s))
            planes.append(t1[re])
            xm.pop(i_imagsym)
        elif i_realsym is not None:
            results.append(_rspole(t1, xm[i_realsym]['k'], s))
            planes.append(Abs(t1[re]))
            xm.pop(i_realsym)
        elif i_pointsym is not None:
            results.append(_sypole(t1, xm[i_pointsym]['k'], s))
            planes.append(Abs(t1[re]))
            xm.pop(i_pointsym)
        else:
            results.append(_simplepole(t1, s))
            planes.append(t1[re])

    return Add(*results), Max(*planes)

