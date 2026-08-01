
def test_extra():
    extra = z.dual*A*z
    assert qapply(Jz*po*extra) == hbar*po*extra
    assert qapply(Jx*z*extra) == (hbar*po/sqrt(2) + hbar*mo/sqrt(2))*extra
    assert qapply(
        (Jplus + Jminus)*z/sqrt(2)*extra) == hbar*po*extra + hbar*mo*extra
    assert qapply(Jz*(po + mo)*extra) == hbar*po*extra - hbar*mo*extra
    assert qapply(Jz*po*extra + Jz*mo*extra) == hbar*po*extra - hbar*mo*extra
    assert qapply(Jminus*Jminus*po*extra) == 2*hbar**2*mo*extra
    assert qapply(Jplus**2*mo*extra) == 2*hbar**2*po*extra
    assert qapply(Jplus**2*Jminus**2*po*extra) == 4*hbar**4*po*extra

