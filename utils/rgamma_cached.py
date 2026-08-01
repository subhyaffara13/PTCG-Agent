
def rgamma_cached(x, dps):
    with mp.workdps(dps):
        return mp.rgamma(x)

