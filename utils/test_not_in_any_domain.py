
def test_not_in_any_domain():
    check = list(_illegal) + [x] + [
        float(i) for i in _illegal[:3]]
    for dom in (ZZ, QQ, RR, CC, EX):
        for i in check:
            if i == x and dom == EX:
                continue
            assert i not in dom, (i, dom)
            raises(CoercionFailed, lambda: dom.convert(i))

