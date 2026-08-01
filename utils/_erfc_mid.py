
def _erfc_mid(x):
    # Rational approximation assuming 0 <= x <= 9
    return exp(-x*x)*_polyval(_erfc_coeff_P,x)/_polyval(_erfc_coeff_Q,x)

