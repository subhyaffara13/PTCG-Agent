
def argus_gamma_trf(x, chi):
    if chi <= 5:
        return x
    return np.sqrt(1.0 - 2 * x / chi**2)

