
def test_hydrogen_energies():
    assert E_nl(n, Z) == -Z**2/(2*n**2)
    assert E_nl(n) == -1/(2*n**2)

    assert E_nl(1, 47) == -S(47)**2/(2*1**2)
    assert E_nl(2, 47) == -S(47)**2/(2*2**2)

    assert E_nl(1) == -S.One/(2*1**2)
    assert E_nl(2) == -S.One/(2*2**2)
    assert E_nl(3) == -S.One/(2*3**2)
    assert E_nl(4) == -S.One/(2*4**2)
    assert E_nl(100) == -S.One/(2*100**2)

    raises(ValueError, lambda: E_nl(0))

