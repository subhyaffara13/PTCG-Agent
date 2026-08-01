
def test_DMP():
    p1 = DMP([1, 2], ZZ)
    p2 = ZZ.old_poly_ring(x)([1, 2])
    if GROUND_TYPES != 'flint':
        assert srepr(p1) == "DMP_Python([1, 2], ZZ)"
        assert srepr(p2) == "DMP_Python([1, 2], ZZ)"
    else:
        assert srepr(p1) == "DUP_Flint([1, 2], ZZ)"
        assert srepr(p2) == "DUP_Flint([1, 2], ZZ)"

