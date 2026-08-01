
def _Phi_Z0(alpha, t):
    return (
        -np.tan(np.pi * alpha / 2) * (np.abs(t) ** (1 - alpha) - 1)
        if alpha != 1
        else -2.0 * np.log(np.abs(t)) / np.pi
    )

