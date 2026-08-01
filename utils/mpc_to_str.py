
def mpc_to_str(z, dps, **kwargs):
    re, im = z
    rs = to_str(re, dps)
    if im[0]:
        return rs + " - " + to_str(mpf_neg(im), dps, **kwargs) + "j"
    else:
        return rs + " + " + to_str(im, dps, **kwargs) + "j"

