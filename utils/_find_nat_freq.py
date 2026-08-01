
def _find_nat_freq(stopb, passb, gpass, gstop, filter_type, filter_kind, *, xp):
    if filter_type == 1:            # low
        nat = stopb / passb
    elif filter_type == 2:          # high
        nat = passb / stopb
    elif filter_type == 3:          # stop

        passb, stopb = np.asarray(passb), np.asarray(stopb)    # XXX fminbound array API
        wp0 = optimize.fminbound(band_stop_obj, passb[0], stopb[0] - 1e-12,
                                 args=(0, passb, stopb, gpass, gstop,
                                       filter_kind),
                                 disp=0)
        wp1 = optimize.fminbound(band_stop_obj, stopb[1] + 1e-12, passb[1],
                                 args=(1, passb, stopb, gpass, gstop,
                                       filter_kind),
                                 disp=0)
        passb = [float(wp0), float(wp1)]
        passb, stopb = xp.asarray(passb), xp.asarray(stopb)
        nat = ((stopb * (passb[0] - passb[1])) /
               (stopb ** 2 - passb[0] * passb[1]))
    elif filter_type == 4:          # pass
        nat = ((stopb ** 2 - passb[0] * passb[1]) /
               (stopb * (passb[0] - passb[1])))
    else:
        raise ValueError(f"should not happen: {filter_type =}.")

    nat = xp.min(xp.abs(nat))
    return nat, passb

