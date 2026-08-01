
def test_SetExpr_Intersection():
    x, y, z, w = symbols("x y z w")
    set1 = Interval(x, y)
    set2 = Interval(w, z)
    inter = Intersection(set1, set2)
    se = SetExpr(inter)
    assert exp(se).set == Intersection(
        ImageSet(Lambda(x, exp(x)), set1),
        ImageSet(Lambda(x, exp(x)), set2))
    assert cos(se).set == ImageSet(Lambda(x, cos(x)), inter)

