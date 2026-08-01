
def test_vector_cross_xfail():
    ACS = CoordSys3D('A')
    assert mathml(Cross(ACS.x, ACS.z) + Cross(ACS.z, ACS.x), printer='presentation') == \
        '<mover><mi mathvariant="bold">0</mi><mo>^</mo></mover>'

