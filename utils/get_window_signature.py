
def get_window_signature(window, Nx, fftbins=True, *, xp=None, device=None):
    return np if xp is None else xp

