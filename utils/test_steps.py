
def test_steps():
    if not np:
        skip("numpy not installed.")

    x, u = symbols("x, u")

    def do_test(s1, s2):
        if (not s1.is_parametric) and s1.is_2Dline:
            xx1, _ = s1.get_data()
            xx2, _ = s2.get_data()
        elif s1.is_parametric and s1.is_2Dline:
            xx1, _, _ = s1.get_data()
            xx2, _, _ = s2.get_data()
        elif (not s1.is_parametric) and s1.is_3Dline:
            xx1, _, _ = s1.get_data()
            xx2, _, _ = s2.get_data()
        else:
            xx1, _, _, _ = s1.get_data()
            xx2, _, _, _ = s2.get_data()
        assert len(xx1) != len(xx2)

    s1 = LineOver1DRangeSeries(cos(x), (x, -5, 5), "",
        adaptive=False, n=40, steps=False)
    s2 = LineOver1DRangeSeries(cos(x), (x, -5, 5), "",
        adaptive=False, n=40, steps=True)
    do_test(s1, s2)

    s1 = List2DSeries([0, 1, 2], [3, 4, 5], steps=False)
    s2 = List2DSeries([0, 1, 2], [3, 4, 5], steps=True)
    do_test(s1, s2)

    s1 = Parametric2DLineSeries(cos(x), sin(x), (x, -5, 5),
        adaptive=False, n=40, steps=False)
    s2 = Parametric2DLineSeries(cos(x), sin(x), (x, -5, 5),
        adaptive=False, n=40, steps=True)
    do_test(s1, s2)

    s1 = Parametric3DLineSeries(cos(x), sin(x), x, (x, -5, 5),
        adaptive=False, n=40, steps=False)
    s2 = Parametric3DLineSeries(cos(x), sin(x), x, (x, -5, 5),
        adaptive=False, n=40, steps=True)
    do_test(s1, s2)

