
def _betai(a, b, x):
    x = np.asanyarray(x)
    x = ma.where(x < 1.0, x, 1.0)  # if x > 1 then return 1.0
    return special.betainc(a, b, x)

