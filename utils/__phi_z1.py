
def _Phi_Z1(alpha, t):
    return (
        np.tan(np.pi * alpha / 2)
        if alpha != 1
        else -2.0 * np.log(np.abs(t)) / np.pi
    )

