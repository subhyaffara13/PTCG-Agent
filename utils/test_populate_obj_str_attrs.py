
def test_populate_obj_str_attrs():
    pop = 1000
    o = types.SimpleNamespace(**{str(i): i for i in range(pop)})
    new_o = m.populate_obj_str_attrs(o, pop)
    new_attrs = {k: v for k, v in new_o.__dict__.items() if not k.startswith("_")}
    assert all(isinstance(v, str) for v in new_attrs.values())
    assert len(new_attrs) == pop

