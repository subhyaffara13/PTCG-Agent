
def test_Divergence():
    assert Divergence(v1) == Divergence(R.x*R.i + R.z*R.z*R.j)
    assert Divergence(v2) == Divergence(R.x*R.i + R.y*R.j + R.z*R.k)
    assert Divergence(v1).doit() == 1
    assert Divergence(v2).doit() == 3
    # issue 22384
    Rc = CoordSys3D('R', transformation='cylindrical')
    assert Divergence(Rc.i).doit() == 1/Rc.r

