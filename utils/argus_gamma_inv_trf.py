
def argus_gamma_inv_trf(x, chi):
    if chi <= 5:
        return x
    return 0.5 * chi**2 * (1 - x**2)

