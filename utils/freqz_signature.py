
def freqz_signature(b, a=1, worN=512, *args, **kwds):
    # differs from freqs: `a` has a default value
    return array_namespace(b, a, worN)

