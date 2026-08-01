
def mod_pi2(man, exp, mag, wp):
    # Reduce to standard interval
    if mag > 0:
        i = 0
        while 1:
            cancellation_prec = 20 << i
            wpmod = wp + mag + cancellation_prec
            pi2 = pi_fixed(wpmod-1)
            pi4 = pi2 >> 1
            offset = wpmod + exp
            if offset >= 0:
                t = man << offset
            else:
                t = man >> (-offset)
            n, y = divmod(t, pi2)
            if y > pi4:
                small = pi2 - y
            else:
                small = y
            if small >> (wp+mag-10):
                n = int(n)
                t = y >> mag
                wp = wpmod - mag
                break
            i += 1
    else:
        wp += (-mag)
        offset = exp + wp
        if offset >= 0:
            t = man << offset
        else:
            t = man >> (-offset)
        n = 0
    return t, n, wp

