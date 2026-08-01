
def lommels2(ctx, u, v, z, **kwargs):
    u = ctx._convert_param(u)[0]
    v = ctx._convert_param(v)[0]
    z = ctx.convert(z)
    # Asymptotic expansion (GR p. 947) -- need to be careful
    # not to use for small arguments
    # def h(u,v):
    #    b = ctx.mpq_1_2
    #    w = -(z/2)**(-2)
    #    return ([z], [u-1], [], [], [b*(1-u+v)], [b*(1-u-v)], w),
    def h(u,v):
        b = ctx.mpq_1_2
        w = ctx.square_exp_arg(z, mult=-0.25)
        T1 = [u-v+1, u+v+1, z], [-1, -1, u+1], [], [], [1], [b*(u-v+3),b*(u+v+3)], w
        T2 = [2, z], [u+v-1, -v], [v, b*(u+v+1)], [b*(v-u+1)], [], [1-v], w
        T3 = [2, z], [u-v-1, v], [-v, b*(u-v+1)], [b*(1-u-v)], [], [1+v], w
        #c1 = ctx.cospi((u-v)*b)
        #c2 = ctx.cospi((u+v)*b)
        #s = ctx.sinpi(v)
        #r1 = (u-v+1)*b
        #r2 = (u+v+1)*b
        #T2 = [c1, s, z, 2], [1, -1, -v, v], [], [-v+1], [], [-v+1], w
        #T3 = [-c2, s, z, 2], [1, -1, v, -v], [], [v+1], [], [v+1], w
        #T2 = [c1, s, z, 2], [1, -1, -v, v+u-1], [r1, r2], [-v+1], [], [-v+1], w
        #T3 = [-c2, s, z, 2], [1, -1, v, -v+u-1], [r1, r2], [v+1], [], [v+1], w
        return T1, T2, T3
    return ctx.hypercomb(h, [u,v], **kwargs)

