
def _coef(ctx, J, eps):
    r"""
    Computes the coefficients  `c_n`  for `0\le n\le 2J` with error less than eps

    **Definition**

    The coefficients c_n are defined by

    .. math ::

        \begin{equation}
        F(z)=\frac{e^{\pi i
        \bigl(\frac{z^2}{2}+\frac38\bigr)}-i\sqrt{2}\cos\frac{\pi}{2}z}{2\cos\pi
        z}=\sum_{n=0}^\infty c_{2n} z^{2n}
        \end{equation}

    they are computed applying the relation

    .. math ::

        \begin{multline}
        c_{2n}=-\frac{i}{\sqrt{2}}\Bigl(\frac{\pi}{2}\Bigr)^{2n}
        \sum_{k=0}^n\frac{(-1)^k}{(2k)!}
        2^{2n-2k}\frac{(-1)^{n-k}E_{2n-2k}}{(2n-2k)!}+\\
        +e^{3\pi i/8}\sum_{j=0}^n(-1)^j\frac{
        E_{2j}}{(2j)!}\frac{i^{n-j}\pi^{n+j}}{(n-j)!2^{n-j+1}}.
        \end{multline}
    """

    newJ = J+2        # compute more coefficients that are needed
    neweps6 = eps/2.  # compute with a slight more precision that are needed

    #  PREPARATION FOR THE COMPUTATION OF V(N) AND W(N)
    #    See II Section 3.16
    #
    #  Computing the exponent wpvw of the error II equation (81)
    wpvw = max(ctx.mag(10*(newJ+3)), 4*newJ+5-ctx.mag(neweps6))

    #  Preparation of Euler numbers (we need until the 2*RS_NEWJ)
    E = ctx._eulernum(2*newJ)

    #  Now we have in the cache all the needed Euler numbers.
    #
    #  Computing the powers of pi
    #
    # We need to compute the powers pi**n for 1<= n <= 2*J
    # with relative error less than 2**(-wpvw)
    # it is easy to show that this is obtained
    # taking wppi as the least d with
    # 2**d>40*J and 2**d> 4.24 *newJ + 2**wpvw
    # In II Section 3.9 we need also that
    #  wppi > wptcoef[0], and that the powers
    # here computed  0<= k <= 2*newJ are more
    # than those needed there that are 2*L-2.
    # so we need  J >= L this will be checked
    # before computing tcoef[]
    wppi = max(ctx.mag(40*newJ), ctx.mag(newJ)+3 +wpvw)
    ctx.prec = wppi
    pipower = {}
    pipower[0] = ctx.one
    pipower[1] = ctx.pi
    for n in range(2,2*newJ+1):
        pipower[n] = pipower[n-1]*ctx.pi

    # COMPUTING THE COEFFICIENTS v(n) AND w(n)
    #  see II equation (61) and equations (81) and (82)
    ctx.prec = wpvw+2
    v={}
    w={}
    for n in range(0,newJ+1):
        va = (-1)**n * ctx._eulernum(2*n)
        va = ctx.mpf(va)/ctx.fac(2*n)
        v[n]=va*pipower[2*n]
    for n in range(0,2*newJ+1):
        wa = ctx.one/ctx.fac(n)
        wa=wa/(2**n)
        w[n]=wa*pipower[n]

    # COMPUTATION OF THE CONVOLUTIONS RS_P1 AND RS_P2
    #  See II Section 3.16
    ctx.prec = 15
    wpp1a = 9 - ctx.mag(neweps6)
    P1 = {}
    for n in range(0,newJ+1):
        ctx.prec = 15
        wpp1 = max(ctx.mag(10*(n+4)),4*n+wpp1a)
        ctx.prec = wpp1
        sump = 0
        for k in range(0,n+1):
            sump += ((-1)**k) * v[k]*w[2*n-2*k]
        P1[n]=((-1)**(n+1))*ctx.j*sump
    P2={}
    for n in range(0,newJ+1):
        ctx.prec = 15
        wpp2 = max(ctx.mag(10*(n+4)),4*n+wpp1a)
        ctx.prec = wpp2
        sump = 0
        for k in range(0,n+1):
            sump += (ctx.j**(n-k)) * v[k]*w[n-k]
        P2[n]=sump
    # COMPUTING THE COEFFICIENTS c[2n]
    # See II Section 3.14
    ctx.prec = 15
    wpc0 = 5 - ctx.mag(neweps6)
    wpc = max(6,4*newJ+wpc0)
    ctx.prec = wpc
    mu = ctx.sqrt(ctx.mpf('2'))/2
    nu = ctx.expjpi(3./8)/2
    c={}
    for n in range(0,newJ):
        ctx.prec = 15
        wpc = max(6,4*n+wpc0)
        ctx.prec = wpc
        c[2*n] = mu*P1[n]+nu*P2[n]
    for n in range(1,2*newJ,2):
        c[n] = 0
    return [newJ, neweps6, c, pipower]

