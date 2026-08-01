
def test_roundtrip_with_dict(cls_name):
    cls = getattr(m, cls_name)
    p = cls("test_value")
    p.extra = 15
    p.dynamic = "Attribute"

    data = pickle.dumps(p, pickle.HIGHEST_PROTOCOL)
    p2 = pickle.loads(data)
    assert p2.value == p.value
    assert p2.extra == p.extra
    assert p2.dynamic == p.dynamic

