
def test_dict_methods_covered(d, Asp):
    d_methods = set(dir(d)) - {"__class_getitem__"}
    asp_methods = set(dir(Asp))
    assert d_methods < asp_methods

