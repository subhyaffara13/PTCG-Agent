
def test_fresnel_series():
    assert fresnelc(z).series(z, n=15) == \
        z - pi**2*z**5/40 + pi**4*z**9/3456 - pi**6*z**13/599040 + O(z**15)

    # issues 6510, 10102
    fs = (S.Half - sin(pi*z**2/2)/(pi**2*z**3)
        + (-1/(pi*z) + 3/(pi**3*z**5))*cos(pi*z**2/2))
    fc = (S.Half - cos(pi*z**2/2)/(pi**2*z**3)
        + (1/(pi*z) - 3/(pi**3*z**5))*sin(pi*z**2/2))
    assert fresnels(z).series(z, oo) == fs + O(z**(-6), (z, oo))
    assert fresnelc(z).series(z, oo) == fc + O(z**(-6), (z, oo))
    assert (fresnels(z).series(z, -oo) + fs.subs(z, -z)).expand().is_Order
    assert (fresnelc(z).series(z, -oo) + fc.subs(z, -z)).expand().is_Order
    assert (fresnels(1/z).series(z) - fs.subs(z, 1/z)).expand().is_Order
    assert (fresnelc(1/z).series(z) - fc.subs(z, 1/z)).expand().is_Order
    assert ((2*fresnels(3*z)).series(z, oo) - 2*fs.subs(z, 3*z)).expand().is_Order
    assert ((3*fresnelc(2*z)).series(z, oo) - 3*fc.subs(z, 2*z)).expand().is_Order

