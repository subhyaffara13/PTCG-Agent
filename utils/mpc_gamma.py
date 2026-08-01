
def mpc_gamma(z, prec, rnd='d', type=0):
    a, b = z
    asign, aman, aexp, abc = a
    bsign, bman, bexp, bbc = b

    if b == fzero:
        # Imaginary part on negative half-axis for log-gamma function
        if type == 3 and asign:
            re = mpf_gamma(a, prec, rnd, 3)
            n = (-aman) >> (-aexp)
            im = mpf_mul_int(mpf_pi(prec+10), n, prec, rnd)
            return re, im
        return mpf_gamma(a, prec, rnd, type), fzero

    # Some kind of complex inf/nan
    if (not aman and aexp) or (not bman and bexp):
        return (fnan, fnan)

    # Initial working precision
    wp = prec + 20

    amag = aexp+abc
    bmag = bexp+bbc
    if aman:
        mag = max(amag, bmag)
    else:
        mag = bmag

    # Close to 0
    if mag < -8:
        if mag < -wp:
            # 1/gamma(z) = z + euler*z^2 + O(z^3)
            v = mpc_add(z, mpc_mul_mpf(mpc_mul(z,z,wp),mpf_euler(wp),wp), wp)
            if type == 0: return mpc_reciprocal(v, prec, rnd)
            if type == 1: return mpc_div(z, v, prec, rnd)
            if type == 2: return mpc_pos(v, prec, rnd)
            if type == 3: return mpc_log(mpc_reciprocal(v, prec), prec, rnd)
        elif type != 1:
            wp += (-mag)

    # Handle huge log-gamma values; must do this before converting to
    # a fixed-point value. TODO: determine a precise cutoff of validity
    # depending on amag and bmag
    if type == 3 and mag > wp and ((not asign) or (bmag >= amag)):
        return mpc_sub(mpc_mul(z, mpc_log(z, wp), wp), z, prec, rnd)

    # From now on, we assume having a gamma function
    if type == 1:
        return mpc_gamma((mpf_add(a, fone), b), prec, rnd, 0)

    an = abs(to_int(a))
    bn = abs(to_int(b))
    absn = max(an, bn)
    gamma_size = absn*mag
    if type == 3:
        pass
    else:
        wp += bitcount(gamma_size)

    # Reflect to the right half-plane. Note that Stirling's expansion
    # is valid in the left half-plane too, as long as we're not too close
    # to the real axis, but in order to use this argument reduction
    # in the negative direction must be implemented.
    #need_reflection = asign and ((bmag < 0) or (amag-bmag > 4))
    need_reflection = asign
    zorig = z
    if need_reflection:
        z = mpc_neg(z)
        asign, aman, aexp, abc = a = z[0]
        bsign, bman, bexp, bbc = b = z[1]

    # Imaginary part very small compared to real one?
    yfinal = 0
    balance_prec = 0
    if bmag < -10:
        # Check z ~= 1 and z ~= 2 for loggamma
        if type == 3:
            zsub1 = mpc_sub_mpf(z, fone)
            if zsub1[0] == fzero:
                cancel1 = -bmag
            else:
                cancel1 = -max(zsub1[0][2]+zsub1[0][3], bmag)
            if cancel1 > wp:
                pi = mpf_pi(wp)
                x = mpc_mul_mpf(zsub1, pi, wp)
                x = mpc_mul(x, x, wp)
                x = mpc_div_mpf(x, from_int(12), wp)
                y = mpc_mul_mpf(zsub1, mpf_neg(mpf_euler(wp)), wp)
                yfinal = mpc_add(x, y, wp)
                if not need_reflection:
                    return mpc_pos(yfinal, prec, rnd)
            elif cancel1 > 0:
                wp += cancel1
            zsub2 = mpc_sub_mpf(z, ftwo)
            if zsub2[0] == fzero:
                cancel2 = -bmag
            else:
                cancel2 = -max(zsub2[0][2]+zsub2[0][3], bmag)
            if cancel2 > wp:
                pi = mpf_pi(wp)
                t = mpf_sub(mpf_mul(pi, pi), from_int(6))
                x = mpc_mul_mpf(mpc_mul(zsub2, zsub2, wp), t, wp)
                x = mpc_div_mpf(x, from_int(12), wp)
                y = mpc_mul_mpf(zsub2, mpf_sub(fone, mpf_euler(wp)), wp)
                yfinal = mpc_add(x, y, wp)
                if not need_reflection:
                    return mpc_pos(yfinal, prec, rnd)
            elif cancel2 > 0:
                wp += cancel2
        if bmag < -wp:
            # Compute directly from the real gamma function.
            pp = 2*(wp+10)
            aabs = mpf_abs(a)
            eps = mpf_shift(fone, amag-wp)
            x1 = mpf_gamma(aabs, pp, type=type)
            x2 = mpf_gamma(mpf_add(aabs, eps), pp, type=type)
            xprime = mpf_div(mpf_sub(x2, x1, pp), eps, pp)
            y = mpf_mul(b, xprime, prec, rnd)
            yfinal = (x1, y)
            # Note: we still need to use the reflection formula for
            # near-poles, and the correct branch of the log-gamma function
            if not need_reflection:
                return mpc_pos(yfinal, prec, rnd)
        else:
            balance_prec += (-bmag)

    wp += balance_prec
    n_for_stirling = int(GAMMA_STIRLING_BETA*wp)
    need_reduction = absn < n_for_stirling

    afix = to_fixed(a, wp)
    bfix = to_fixed(b, wp)

    r = 0
    if not yfinal:
        zprered = z
        # Argument reduction
        if absn < n_for_stirling:
            absn = complex(an, bn)
            d = int((1 + n_for_stirling**2 - bn**2)**0.5 - an)
            rre = one = MPZ_ONE << wp
            rim = MPZ_ZERO
            for k in xrange(d):
                rre, rim = ((afix*rre-bfix*rim)>>wp), ((afix*rim + bfix*rre)>>wp)
                afix += one
            r = from_man_exp(rre, -wp), from_man_exp(rim, -wp)
            a = from_man_exp(afix, -wp)
            z = a, b

        yre, yim = complex_stirling_series(afix, bfix, wp)
        # (z-1/2)*log(z) + S
        lre, lim = mpc_log(z, wp)
        lre = to_fixed(lre, wp)
        lim = to_fixed(lim, wp)
        yre = ((lre*afix - lim*bfix)>>wp) - (lre>>1) + yre
        yim = ((lre*bfix + lim*afix)>>wp) - (lim>>1) + yim
        y = from_man_exp(yre, -wp), from_man_exp(yim, -wp)

        if r and type == 3:
            # If re(z) > 0 and abs(z) <= 4, the branches of loggamma(z)
            # and log(gamma(z)) coincide. Otherwise, use the zeroth order
            # Stirling expansion to compute the correct imaginary part.
            y = mpc_sub(y, mpc_log(r, wp), wp)
            zfa = to_float(zprered[0])
            zfb = to_float(zprered[1])
            zfabs = math.hypot(zfa,zfb)
            #if not (zfa > 0.0 and zfabs <= 4):
            yfb = to_float(y[1])
            u = math.atan2(zfb, zfa)
            if zfabs <= 0.5:
                gi = 0.577216*zfb - u
            else:
                gi = -zfb - 0.5*u + zfa*u + zfb*math.log(zfabs)
            n = int(math.floor((gi-yfb)/(2*math.pi)+0.5))
            y = (y[0], mpf_add(y[1], mpf_mul_int(mpf_pi(wp), 2*n, wp), wp))

    if need_reflection:
        if type == 0 or type == 2:
            A = mpc_mul(mpc_sin_pi(zorig, wp), zorig, wp)
            B = (mpf_neg(mpf_pi(wp)), fzero)
            if yfinal:
                if type == 2:
                    A = mpc_div(A, yfinal, wp)
                else:
                    A = mpc_mul(A, yfinal, wp)
            else:
                A = mpc_mul(A, mpc_exp(y, wp), wp)
            if r:
                B = mpc_mul(B, r, wp)
            if type == 0: return mpc_div(B, A, prec, rnd)
            if type == 2: return mpc_div(A, B, prec, rnd)

        # Reflection formula for the log-gamma function with correct branch
        # http://functions.wolfram.com/GammaBetaErf/LogGamma/16/01/01/0006/
        # LogGamma[z] == -LogGamma[-z] - Log[-z] +
        # Sign[Im[z]] Floor[Re[z]] Pi I + Log[Pi] -
        #      Log[Sin[Pi (z - Floor[Re[z]])]] -
        # Pi I (1 - Abs[Sign[Im[z]]]) Abs[Floor[Re[z]]]
        if type == 3:
            if yfinal:
                s1 = mpc_neg(yfinal)
            else:
                s1 = mpc_neg(y)
            # s -= log(-z)
            s1 = mpc_sub(s1, mpc_log(mpc_neg(zorig), wp), wp)
            # floor(re(z))
            rezfloor = mpf_floor(zorig[0])
            imzsign = mpf_sign(zorig[1])
            pi = mpf_pi(wp)
            t = mpf_mul(pi, rezfloor)
            t = mpf_mul_int(t, imzsign, wp)
            s1 = (s1[0], mpf_add(s1[1], t, wp))
            s1 = mpc_add_mpf(s1, mpf_log(pi, wp), wp)
            t = mpc_sin_pi(mpc_sub_mpf(zorig, rezfloor), wp)
            t = mpc_log(t, wp)
            s1 = mpc_sub(s1, t, wp)
            # Note: may actually be unused, because we fall back
            # to the mpf_ function for real arguments
            if not imzsign:
                t = mpf_mul(pi, mpf_floor(rezfloor), wp)
                s1 = (s1[0], mpf_sub(s1[1], t, wp))
            return mpc_pos(s1, prec, rnd)
    else:
        if type == 0:
            if r:
                return mpc_div(mpc_exp(y, wp), r, prec, rnd)
            return mpc_exp(y, prec, rnd)
        if type == 2:
            if r:
                return mpc_div(r, mpc_exp(y, wp), prec, rnd)
            return mpc_exp(mpc_neg(y), prec, rnd)
        if type == 3:
            return mpc_pos(y, prec, rnd)

