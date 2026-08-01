
def ellipe(ctx, *args):
    r"""
    Called with a single argument `m`, evaluates the Legendre complete
    elliptic integral of the second kind, `E(m)`, defined by

        .. math :: E(m) = \int_0^{\pi/2} \sqrt{1-m \sin^2 t} \, dt \,=\,
            \frac{\pi}{2}
            \,_2F_1\left(\frac{1}{2}, -\frac{1}{2}, 1, m\right).

    Called with two arguments `\phi, m`, evaluates the incomplete elliptic
    integral of the second kind

     .. math ::

        E(\phi,m) = \int_0^{\phi} \sqrt{1-m \sin^2 t} \, dt =
                    \int_0^{\sin z}
                    \frac{\sqrt{1-mt^2}}{\sqrt{1-t^2}} \, dt.

    The incomplete integral reduces to a complete integral when
    `\phi = \frac{\pi}{2}`; that is,

    .. math ::

        E\left(\frac{\pi}{2}, m\right) = E(m).

    In the defining integral, it is assumed that the principal branch
    of the square root is taken and that the path of integration avoids
    crossing any branch cuts. Outside `-\pi/2 \le \Re(z) \le \pi/2`,
    the function extends quasi-periodically as

    .. math ::

        E(\phi + n \pi, m) = 2 n E(m) + E(\phi,m), n \in \mathbb{Z}.

    **Plots**

    .. literalinclude :: /plots/ellipe.py
    .. image :: /plots/ellipe.png

    **Examples for the complete integral**

    Basic values and limits::

        >>> from mpmath import *
        >>> mp.dps = 25; mp.pretty = True
        >>> ellipe(0)
        1.570796326794896619231322
        >>> ellipe(1)
        1.0
        >>> ellipe(-1)
        1.910098894513856008952381
        >>> ellipe(2)
        (0.5990701173677961037199612 + 0.5990701173677961037199612j)
        >>> ellipe(inf)
        (0.0 + +infj)
        >>> ellipe(-inf)
        +inf

    Verifying the defining integral and hypergeometric
    representation::

        >>> ellipe(0.5)
        1.350643881047675502520175
        >>> quad(lambda t: sqrt(1-0.5*sin(t)**2), [0, pi/2])
        1.350643881047675502520175
        >>> pi/2*hyp2f1(0.5,-0.5,1,0.5)
        1.350643881047675502520175

    Evaluation is supported for arbitrary complex `m`::

        >>> ellipe(0.5+0.25j)
        (1.360868682163129682716687 - 0.1238733442561786843557315j)
        >>> ellipe(3+4j)
        (1.499553520933346954333612 - 1.577879007912758274533309j)

    A definite integral::

        >>> quad(ellipe, [0,1])
        1.333333333333333333333333

    **Examples for the incomplete integral**

    Basic values and limits::

        >>> ellipe(0,1)
        0.0
        >>> ellipe(0,0)
        0.0
        >>> ellipe(1,0)
        1.0
        >>> ellipe(2+3j,0)
        (2.0 + 3.0j)
        >>> ellipe(1,1); sin(1)
        0.8414709848078965066525023
        0.8414709848078965066525023
        >>> ellipe(pi/2, -0.5); ellipe(-0.5)
        1.751771275694817862026502
        1.751771275694817862026502
        >>> ellipe(pi/2, 1); ellipe(-pi/2, 1)
        1.0
        -1.0
        >>> ellipe(1.5, 1)
        0.9974949866040544309417234

    Comparing with numerical integration::

        >>> z,m = 0.5, 1.25
        >>> ellipe(z,m)
        0.4740152182652628394264449
        >>> quad(lambda t: sqrt(1-m*sin(t)**2), [0,z])
        0.4740152182652628394264449

    The arguments may be complex numbers::

        >>> ellipe(3j, 0.5)
        (0.0 + 7.551991234890371873502105j)
        >>> ellipe(3+4j, 5-6j)
        (24.15299022574220502424466 + 75.2503670480325997418156j)
        >>> k = 35
        >>> z,m = 2+3j, 1.25
        >>> ellipe(z+pi*k,m); ellipe(z,m) + 2*k*ellipe(m)
        (48.30138799412005235090766 + 17.47255216721987688224357j)
        (48.30138799412005235090766 + 17.47255216721987688224357j)

    For `|\Re(z)| < \pi/2`, the function can be expressed as a
    hypergeometric series of two variables
    (see :func:`~mpmath.appellf1`)::

        >>> z,m = 0.5, 0.25
        >>> ellipe(z,m)
        0.4950017030164151928870375
        >>> sin(z)*appellf1(0.5,0.5,-0.5,1.5,sin(z)**2,m*sin(z)**2)
        0.4950017030164151928870376

    """
    if len(args) == 1:
        return ctx._ellipe(args[0])
    else:
        phi, m = args
    z = phi
    if not (ctx.isnormal(z) and ctx.isnormal(m)):
        if m == 0:
            return z + m
        if z == 0:
            return z * m
        if m == ctx.inf or m == ctx.ninf:
            return ctx.inf
        raise ValueError
    x = z.real
    ctx.prec += max(0, ctx.mag(x))
    pi = +ctx.pi
    away = abs(x) > pi/2
    if away:
        d = ctx.nint(x/pi)
        z = z-pi*d
        P = 2*d*ctx.ellipe(m)
    else:
        P = 0
    def terms():
        c, s = ctx.cos_sin(z)
        x = c**2
        y = 1-m*s**2
        RF = ctx.elliprf(x, y, 1)
        RD = ctx.elliprd(x, y, 1)
        return s*RF, -m*s**3*RD/3
    return ctx.sum_accurately(terms) + P

