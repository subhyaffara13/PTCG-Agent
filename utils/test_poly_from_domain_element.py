
def test_poly_from_domain_element():
    dom = ZZ[x]
    assert Poly(dom(x+1), y, domain=dom).rep == DMP([dom(x+1)], dom)
    dom = dom.get_field()
    assert Poly(dom(x+1), y, domain=dom).rep == DMP([dom(x+1)], dom)

    dom = QQ[x]
    assert Poly(dom(x+1), y, domain=dom).rep == DMP([dom(x+1)], dom)
    dom = dom.get_field()
    assert Poly(dom(x+1), y, domain=dom).rep == DMP([dom(x+1)], dom)

    dom = ZZ.old_poly_ring(x)
    assert Poly(dom([ZZ(1), ZZ(1)]), y, domain=dom).rep == DMP([dom([ZZ(1), ZZ(1)])], dom)
    dom = dom.get_field()
    assert Poly(dom([ZZ(1), ZZ(1)]), y, domain=dom).rep == DMP([dom([ZZ(1), ZZ(1)])], dom)

    dom = QQ.old_poly_ring(x)
    assert Poly(dom([QQ(1), QQ(1)]), y, domain=dom).rep == DMP([dom([QQ(1), QQ(1)])], dom)
    dom = dom.get_field()
    assert Poly(dom([QQ(1), QQ(1)]), y, domain=dom).rep == DMP([dom([QQ(1), QQ(1)])], dom)

    dom = QQ.algebraic_field(I)
    assert Poly(dom([1, 1]), x, domain=dom).rep == DMP([dom([1, 1])], dom)

