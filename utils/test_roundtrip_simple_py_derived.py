
def test_roundtrip_simple_py_derived():
    p = SimplePyDerived()
    p.num = 202
    p.stored_in_dict = 303
    data = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
    p2 = pickle.loads(data)
    assert isinstance(p2, SimplePyDerived)
    assert p2.num == 202
    assert p2.stored_in_dict == 303

