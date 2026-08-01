
def airybi(ctx, z, derivative=0, **kwargs):
    z = ctx.convert(z)
    if derivative:
        n, ntype = ctx._convert_param(derivative)
    else:
        n = 0
    # Values at infinities
    if not ctx.isnormal(z) and z:
        if n and ntype == 'Z':
            if z == ctx.inf:
                return z
            if z == ctx.ninf:
                if n == -1:
                    return 1/z
                if n == -2:
                    return _airybi_n2_inf(ctx)
                if n < -2:
                    return (-1)**n * (-z)
        if not n:
            if z == ctx.inf:
                return z
            if z == ctx.ninf:
                return 1/z
        # TODO: limits
        raise ValueError("essential singularity of Bi(z)")
    if z:
        extraprec = max(0, int(1.5*ctx.mag(z)))
    else:
        extraprec = 0
    if n:
        if n == 1:
            # http://functions.wolfram.com/03.08.26.0001.01
            def h():
                ctx.prec += extraprec
                w = z**3 / 9
                ctx.prec -= extraprec
                C1 = _airybi_C1(ctx)*0.5
                C2 = _airybi_C2(ctx)
                T1 = [C1,z],[1,2],[],[],[],[ctx.mpq_5_3],w
                T2 = [C2],[1],[],[],[],[ctx.mpq_1_3],w
                return T1, T2
            return ctx.hypercomb(h, [], **kwargs)
        else:
            if z == 0:
                return _airyderiv_0(ctx, z, n, ntype, 1)
            def h(n):
                ctx.prec += extraprec
                w = z**3/9
                ctx.prec -= extraprec
                q13,q23,q43 = ctx.mpq_1_3, ctx.mpq_2_3, ctx.mpq_4_3
                q16 = ctx.mpq_1_6
                q56 = ctx.mpq_5_6
                a1=q13; a2=1; b1=(1-n)*q13; b2=(2-n)*q13; b3=1-n*q13
                T1 = [3, z], [n-q16, -n], [a1], [b1,b2,b3], \
                    [a1,a2], [b1,b2,b3], w
                a1=q23; b1=(2-n)*q13; b2=1-n*q13; b3=(4-n)*q13
                T2 = [3, z], [n-q56, 1-n], [a1], [b1,b2,b3], \
                    [a1,a2], [b1,b2,b3], w
                return T1, T2
            v = ctx.hypercomb(h, [n], **kwargs)
            if ctx._is_real_type(z) and ctx.isint(n):
                v = ctx._re(v)
            return v
    else:
        def h():
            ctx.prec += extraprec
            w = z**3 / 9
            ctx.prec -= extraprec
            C1 = _airybi_C1(ctx)
            C2 = _airybi_C2(ctx)
            T1 = [C1],[1],[],[],[],[ctx.mpq_2_3],w
            T2 = [z*C2],[1],[],[],[],[ctx.mpq_4_3],w
            return T1, T2
        return ctx.hypercomb(h, [], **kwargs)

