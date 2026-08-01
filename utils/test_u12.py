
def test_U12():
    # Wester sample case:
    # (c41) /* d(3 x^5 dy /\ dz + 5 x y^2 dz /\ dx + 8 z dx /\ dy)
    #    => (15 x^4 + 10 x y + 8) dx /\ dy /\ dz */
    # factor(ext_diff(3*x^5 * dy ~ dz + 5*x*y^2 * dz ~ dx + 8*z * dx ~ dy));
    #                      4
    # (d41)              (10 x y + 15 x  + 8) dx dy dz
    raise NotImplementedError(
        "External diff of differential form not supported")

