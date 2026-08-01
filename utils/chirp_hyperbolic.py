
def chirp_hyperbolic(t, f0, f1, t1):
    f = f0*f1*t1 / ((f0 - f1)*t + f1*t1)
    return f

