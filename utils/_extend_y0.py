
def _extend_y0(Holonomic, n):
    """
    Tries to find more initial conditions by substituting the initial
    value point in the differential equation.
    """

    if Holonomic.annihilator.is_singular(Holonomic.x0) or Holonomic.is_singularics() == True:
        return Holonomic.y0

    annihilator = Holonomic.annihilator
    a = annihilator.order

    listofpoly = []

    y0 = Holonomic.y0
    R = annihilator.parent.base
    K = R.get_field()

    for j in annihilator.listofpoly:
        if isinstance(j, annihilator.parent.base.dtype):
            listofpoly.append(K.new(j.to_list()))

    if len(y0) < a or n <= len(y0):
        return y0
    list_red = [-listofpoly[i] / listofpoly[a]
                for i in range(a)]
    y1 = y0[:min(len(y0), a)]
    for _ in range(n - a):
        sol = 0
        for a, b in zip(y1, list_red):
            r = DMFsubs(b, Holonomic.x0)
            if not getattr(r, 'is_finite', True):
                return y0
            if isinstance(r, (PolyElement, FracElement)):
                r = r.as_expr()
            sol += a * r
        y1.append(sol)
        list_red = _derivate_diff_eq(list_red, K)
    return y0 + y1[len(y0):]

