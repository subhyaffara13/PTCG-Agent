
def _postprocess_wn(WN, analog, fs, *, xp):
    wn = WN if analog else xp.atan(WN) * 2.0 / xp.pi
    if wn.shape[0] == 1:
        wn = wn[0]
    if fs is not None:
        wn = wn * fs / 2
    return wn

