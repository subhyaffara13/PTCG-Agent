
def _assert_poles_close(P1,P2, rtol=1e-8, atol=1e-8):
    """
    Check each pole in P1 is close to a pole in P2 with a 1e-8
    relative tolerance or 1e-8 absolute tolerance (useful for zero poles).
    These tolerances are very strict but the systems tested are known to
    accept these poles so we should not be far from what is requested.
    """
    P2 = P2.copy()
    for p1 in P1:
        found = False
        for p2_idx in range(P2.shape[0]):
            if np.allclose([np.real(p1), np.imag(p1)],
                           [np.real(P2[p2_idx]), np.imag(P2[p2_idx])],
                           rtol, atol):
                found = True
                np.delete(P2, p2_idx)
                break
        if not found:
            raise ValueError("Can't find pole " + str(p1) + " in " + str(P2))

