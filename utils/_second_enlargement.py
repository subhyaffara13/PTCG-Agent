
def _second_enlargement(H, p, q):
    r"""
    Perform the second enlargement in the Round Two algorithm.
    """
    Ip = nilradical_mod_p(H, p, q=q)
    B = H.parent.submodule_from_matrix(H.matrix * Ip.matrix, denom=H.denom)
    C = B + p*H
    E = C.endomorphism_ring()
    phi = ModuleHomomorphism(H, E, lambda x: E.inner_endomorphism(x))
    gamma = phi.kernel(modulus=p)
    G = H.parent.submodule_from_matrix(H.matrix * gamma.matrix, denom=H.denom * p)
    H1 = G + H
    return H1, Ip

