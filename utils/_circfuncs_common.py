
def _circfuncs_common(samples, period, xp=None):
    xp = array_namespace(samples) if xp is None else xp

    samples = xp_promote(samples, force_floating=True, xp=xp)

    # Recast samples as radians that range between 0 and 2 pi and calculate
    # the sine and cosine
    scaled_samples = samples * ((2.0 * pi) / period)
    sin_samp = xp.sin(scaled_samples)
    cos_samp = xp.cos(scaled_samples)

    return samples, sin_samp, cos_samp

