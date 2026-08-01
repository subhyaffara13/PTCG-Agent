
def test_forces():
    a = Arch((0,0),(40,0),crown_x=20,crown_y=12)
    a.apply_load(-1,'C',8,150,angle=270)
    a.apply_load(0,'D',start=20,end=40,mag=-4)
    a.solve()
    assert abs(a.axial_force_at(7.999999999999999)-149.430523405935) < 1e-12
    assert abs(a.shear_force_at(7.999999999999999)-64.9227473161196) < 1e-12

