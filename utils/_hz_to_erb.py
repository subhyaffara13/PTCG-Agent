
def _hz_to_erb(hz):
    """
    Utility for converting from frequency (Hz) to the
    Equivalent Rectangular Bandwidth (ERB) scale
    ERB = frequency / EarQ + minBW
    """
    EarQ = 9.26449
    minBW = 24.7
    return hz / EarQ + minBW

