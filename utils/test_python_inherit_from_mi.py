
def test_python_inherit_from_mi():
    """Tests extending a Python class from a single inheritor of a MI class"""

    class PyMVF(m.MVF):
        g = 7

        def get_g_g(self):
            return self.g

    o = PyMVF()

    assert o.b == 1
    assert o.c == 2
    assert o.d0 == 3
    assert o.d1 == 4
    assert o.e == 5
    assert o.f == 6
    assert o.g == 7

    assert o.get_g_g() == 7

