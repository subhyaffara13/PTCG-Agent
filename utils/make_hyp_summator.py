
def make_hyp_summator(key):
    """
    Returns a function that sums a generalized hypergeometric series,
    for given parameter types (integer, rational, real, complex).

    """
    p, q, param_types, ztype = key

    pstring = "".join(param_types)
    fname = "hypsum_%i_%i_%s_%s_%s" % (p, q, pstring[:p], pstring[p:], ztype)
    #print "generating hypsum", fname

    have_complex_param = 'C' in param_types
    have_complex_arg = ztype == 'C'
    have_complex = have_complex_param or have_complex_arg

    source = []
    add = source.append

    aint = []
    arat = []
    bint = []
    brat = []
    areal = []
    breal = []
    acomplex = []
    bcomplex = []

    #add("wp = prec + 40")
    add("MAX = kwargs.get('maxterms', wp*100)")
    add("HIGH = MPZ_ONE<<epsshift")
    add("LOW = -HIGH")

    # Setup code
    add("SRE = PRE = one = (MPZ_ONE << wp)")
    if have_complex:
        add("SIM = PIM = MPZ_ZERO")

    if have_complex_arg:
        add("xsign, xm, xe, xbc = z[0]")
        add("if xsign: xm = -xm")
        add("ysign, ym, ye, ybc = z[1]")
        add("if ysign: ym = -ym")
    else:
        add("xsign, xm, xe, xbc = z")
        add("if xsign: xm = -xm")

    add("offset = xe + wp")
    add("if offset >= 0:")
    add("    ZRE = xm << offset")
    add("else:")
    add("    ZRE = xm >> (-offset)")
    if have_complex_arg:
        add("offset = ye + wp")
        add("if offset >= 0:")
        add("    ZIM = ym << offset")
        add("else:")
        add("    ZIM = ym >> (-offset)")

    for i, flag in enumerate(param_types):
        W = ["A", "B"][i >= p]
        if flag == 'Z':
            ([aint,bint][i >= p]).append(i)
            add("%sINT_%i = coeffs[%i]" % (W, i, i))
        elif flag == 'Q':
            ([arat,brat][i >= p]).append(i)
            add("%sP_%i, %sQ_%i = coeffs[%i]._mpq_" % (W, i, W, i, i))
        elif flag == 'R':
            ([areal,breal][i >= p]).append(i)
            add("xsign, xm, xe, xbc = coeffs[%i]._mpf_" % i)
            add("if xsign: xm = -xm")
            add("offset = xe + wp")
            add("if offset >= 0:")
            add("    %sREAL_%i = xm << offset" % (W, i))
            add("else:")
            add("    %sREAL_%i = xm >> (-offset)" % (W, i))
        elif flag == 'C':
            ([acomplex,bcomplex][i >= p]).append(i)
            add("__re, __im = coeffs[%i]._mpc_" % i)
            add("xsign, xm, xe, xbc = __re")
            add("if xsign: xm = -xm")
            add("ysign, ym, ye, ybc = __im")
            add("if ysign: ym = -ym")

            add("offset = xe + wp")
            add("if offset >= 0:")
            add("    %sCRE_%i = xm << offset" % (W, i))
            add("else:")
            add("    %sCRE_%i = xm >> (-offset)" % (W, i))
            add("offset = ye + wp")
            add("if offset >= 0:")
            add("    %sCIM_%i = ym << offset" % (W, i))
            add("else:")
            add("    %sCIM_%i = ym >> (-offset)" % (W, i))
        else:
            raise ValueError

    l_areal = len(areal)
    l_breal = len(breal)
    cancellable_real = min(l_areal, l_breal)
    noncancellable_real_num = areal[cancellable_real:]
    noncancellable_real_den = breal[cancellable_real:]

    # LOOP
    add("for n in xrange(1,10**8):")

    add("    if n in magnitude_check:")
    add("        p_mag = bitcount(abs(PRE))")
    if have_complex:
        add("        p_mag = max(p_mag, bitcount(abs(PIM)))")
    add("        magnitude_check[n] = wp-p_mag")

    # Real factors
    multiplier = " * ".join(["AINT_#".replace("#", str(i)) for i in aint] + \
                            ["AP_#".replace("#", str(i)) for i in arat] + \
                            ["BQ_#".replace("#", str(i)) for i in brat])

    divisor    = " * ".join(["BINT_#".replace("#", str(i)) for i in bint] + \
                            ["BP_#".replace("#", str(i)) for i in brat] + \
                            ["AQ_#".replace("#", str(i)) for i in arat] + ["n"])

    if multiplier:
        add("    mul = " + multiplier)
    add("    div = " + divisor)

    # Check for singular terms
    add("    if not div:")
    if multiplier:
        add("        if not mul:")
        add("            break")
    add("        raise ZeroDivisionError")

    # Update product
    if have_complex:

        # TODO: when there are several real parameters and just a few complex
        # (maybe just the complex argument), we only need to do about
        # half as many ops if we accumulate the real factor in a single real variable
        for k in range(cancellable_real): add("    PRE = PRE * AREAL_%i // BREAL_%i" % (areal[k], breal[k]))
        for i in noncancellable_real_num: add("    PRE = (PRE * AREAL_#) >> wp".replace("#", str(i)))
        for i in noncancellable_real_den: add("    PRE = (PRE << wp) // BREAL_#".replace("#", str(i)))
        for k in range(cancellable_real): add("    PIM = PIM * AREAL_%i // BREAL_%i" % (areal[k], breal[k]))
        for i in noncancellable_real_num: add("    PIM = (PIM * AREAL_#) >> wp".replace("#", str(i)))
        for i in noncancellable_real_den: add("    PIM = (PIM << wp) // BREAL_#".replace("#", str(i)))

        if multiplier:
            if have_complex_arg:
                add("    PRE, PIM = (mul*(PRE*ZRE-PIM*ZIM))//div, (mul*(PIM*ZRE+PRE*ZIM))//div")
                add("    PRE >>= wp")
                add("    PIM >>= wp")
            else:
                add("    PRE = ((mul * PRE * ZRE) >> wp) // div")
                add("    PIM = ((mul * PIM * ZRE) >> wp) // div")
        else:
            if have_complex_arg:
                add("    PRE, PIM = (PRE*ZRE-PIM*ZIM)//div, (PIM*ZRE+PRE*ZIM)//div")
                add("    PRE >>= wp")
                add("    PIM >>= wp")
            else:
                add("    PRE = ((PRE * ZRE) >> wp) // div")
                add("    PIM = ((PIM * ZRE) >> wp) // div")

        for i in acomplex:
            add("    PRE, PIM = PRE*ACRE_#-PIM*ACIM_#, PIM*ACRE_#+PRE*ACIM_#".replace("#", str(i)))
            add("    PRE >>= wp")
            add("    PIM >>= wp")

        for i in bcomplex:
            add("    mag = BCRE_#*BCRE_#+BCIM_#*BCIM_#".replace("#", str(i)))
            add("    re = PRE*BCRE_# + PIM*BCIM_#".replace("#", str(i)))
            add("    im = PIM*BCRE_# - PRE*BCIM_#".replace("#", str(i)))
            add("    PRE = (re << wp) // mag".replace("#", str(i)))
            add("    PIM = (im << wp) // mag".replace("#", str(i)))

    else:
        for k in range(cancellable_real): add("    PRE = PRE * AREAL_%i // BREAL_%i" % (areal[k], breal[k]))
        for i in noncancellable_real_num: add("    PRE = (PRE * AREAL_#) >> wp".replace("#", str(i)))
        for i in noncancellable_real_den: add("    PRE = (PRE << wp) // BREAL_#".replace("#", str(i)))
        if multiplier:
            add("    PRE = ((PRE * mul * ZRE) >> wp) // div")
        else:
            add("    PRE = ((PRE * ZRE) >> wp) // div")

    # Add product to sum
    if have_complex:
        add("    SRE += PRE")
        add("    SIM += PIM")
        add("    if (HIGH > PRE > LOW) and (HIGH > PIM > LOW):")
        add("        break")
    else:
        add("    SRE += PRE")
        add("    if HIGH > PRE > LOW:")
        add("        break")

    #add("    from mpmath import nprint, log, ldexp")
    #add("    nprint([n, log(abs(PRE),2), ldexp(PRE,-wp)])")

    add("    if n > MAX:")
    add("        raise NoConvergence('Hypergeometric series converges too slowly. Try increasing maxterms.')")

    # +1 all parameters for next loop
    for i in aint:     add("    AINT_# += 1".replace("#", str(i)))
    for i in bint:     add("    BINT_# += 1".replace("#", str(i)))
    for i in arat:     add("    AP_# += AQ_#".replace("#", str(i)))
    for i in brat:     add("    BP_# += BQ_#".replace("#", str(i)))
    for i in areal:    add("    AREAL_# += one".replace("#", str(i)))
    for i in breal:    add("    BREAL_# += one".replace("#", str(i)))
    for i in acomplex: add("    ACRE_# += one".replace("#", str(i)))
    for i in bcomplex: add("    BCRE_# += one".replace("#", str(i)))

    if have_complex:
        add("a = from_man_exp(SRE, -wp, prec, 'n')")
        add("b = from_man_exp(SIM, -wp, prec, 'n')")

        add("if SRE:")
        add("    if SIM:")
        add("        magn = max(a[2]+a[3], b[2]+b[3])")
        add("    else:")
        add("        magn = a[2]+a[3]")
        add("elif SIM:")
        add("    magn = b[2]+b[3]")
        add("else:")
        add("    magn = -wp+1")

        add("return (a, b), True, magn")
    else:
        add("a = from_man_exp(SRE, -wp, prec, 'n')")

        add("if SRE:")
        add("    magn = a[2]+a[3]")
        add("else:")
        add("    magn = -wp+1")

        add("return a, False, magn")

    source = "\n".join(("    " + line) for line in source)
    source = ("def %s(coeffs, z, prec, wp, epsshift, magnitude_check, **kwargs):\n" % fname) + source

    namespace = {}

    exec_(source, globals(), namespace)

    #print source
    return source, namespace[fname]

