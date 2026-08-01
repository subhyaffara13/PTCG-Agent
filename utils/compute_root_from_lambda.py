
def compute_root_from_lambda(lamb):
    tmp = math.sqrt(3 + 144 * lamb)
    xi = 1 - 96 * lamb + 24 * lamb * tmp
    omega = math.atan(math.sqrt((144 * lamb - 1.0) / xi))
    tmp2 = math.sqrt(xi)
    r = ((24 * lamb - 1 - tmp2) / (24 * lamb) *
         math.sqrt(48*lamb + 24 * lamb * tmp) / tmp2)
    return r, omega

