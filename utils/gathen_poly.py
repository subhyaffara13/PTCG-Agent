
def gathen_poly(n, p, K):
    return gf_from_dict({n: K.one, 1: K.one, 0: K.one}, p, K)

