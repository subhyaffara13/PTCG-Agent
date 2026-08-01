
def _drv2_ppfsingle(self, q, *args):  # Use basic bisection algorithm
    _a, _b = self._get_support(*args)
    b = _b
    a = _a

    step = 10
    if isinf(b):            # Be sure ending point is > q
        b = float(max(100*q, 10))
        while 1:
            if b >= _b:
                qb = 1.0
                break
            qb = self._cdf(b, *args)
            if (qb < q):
                b += step
                step *= 2
            else:
                break
    else:
        qb = 1.0

    step = 10
    if isinf(a):    # be sure starting point < q
        a = float(min(-100*q, -10))
        while 1:
            if a <= _a:
                qb = 0.0
                break
            qa = self._cdf(a, *args)
            if (qa > q):
                a -= step
                step *= 2
            else:
                break
    else:
        qa = self._cdf(a, *args)

    if np.isinf(a) or np.isinf(b):
        message = "Arguments that bracket the requested quantile could not be found."
        raise RuntimeError(message)

    # maximum number of bisections within the normal float64s
    # maxiter = int(np.log2(finfo.max) - np.log2(finfo.smallest_normal))
    maxiter = 2046
    for i in range(maxiter):
        if (qa == q):
            return a
        if (qb == q):
            return b
        if b <= a+1:
            if qa > q:
                return a
            else:
                return b
        c = int((a+b)/2.0)
        qc = self._cdf(c, *args)
        if (qc < q):
            if a != c:
                a = c
            else:
                raise RuntimeError('updating stopped, endless loop')
            qa = qc
        elif (qc > q):
            if b != c:
                b = c
            else:
                raise RuntimeError('updating stopped, endless loop')
            qb = qc
        else:
            return c

