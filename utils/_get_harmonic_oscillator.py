
def _get_harmonic_oscillator():
    def f(t, y):
        return [y[1], -y[0]]

    def event(t, y):
        return y[0]

    return f, event

