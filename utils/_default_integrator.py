
def _default_integrator(f, x):
    return integrate(f, (x, S.Zero, S.Infinity))

