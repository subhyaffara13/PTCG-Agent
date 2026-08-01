
def chirp_geometric(t, f0, f1, t1):
    f = f0 * (f1/f0)**(t/t1)
    return f

