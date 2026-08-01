
def mathieu_mc1_scaled(m, q, x):
    # GSL follows a different normalization.
    # We follow Abramowitz & Stegun, they apparently something else.
    return mathieu_modcem1(m, q, x)[0] * np.sqrt(np.pi/2)

