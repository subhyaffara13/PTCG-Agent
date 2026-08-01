
def test_Quaternion_str_printer():
    q = Quaternion(x, y, z, t)
    assert str(q) == "x + y*i + z*j + t*k"
    q = Quaternion(x,y,z,x*t)
    assert str(q) == "x + y*i + z*j + t*x*k"
    q = Quaternion(x,y,z,x+t)
    assert str(q) == "x + y*i + z*j + (t + x)*k"

