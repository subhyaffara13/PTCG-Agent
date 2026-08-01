
def _single_zpksos(z, p, k):
    """Create one second-order section from up to two zeros and poles"""
    sos = np.zeros(6)
    b, a = zpk2tf(z, p, k)
    sos[3-len(b):3] = b
    sos[6-len(a):6] = a
    return sos

