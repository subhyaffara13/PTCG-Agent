
def test_extend():
    ms = DimensionSystem((length, time), (velocity,))

    mks = ms.extend((mass,), (action,))

    res = DimensionSystem((length, time, mass), (velocity, action))
    assert mks.base_dims == res.base_dims
    assert mks.derived_dims == res.derived_dims


def test_extend():
    ms = UnitSystem((m, s), (c,))
    Js = Quantity("Js")
    Js.set_global_relative_scale_factor(1, joule*second)
    mks = ms.extend((kg,), (Js,))

    res = UnitSystem((m, s, kg), (c, Js))
    assert set(mks._base_units) == set(res._base_units)
    assert set(mks._units) == set(res._units)


def test_extend():
    obj = lambda : my_fn(34)
    assert obj() == 578

    obj_io = StringIO()
    pickler = pickle.Pickler(obj_io)
    pickler.dump(obj)

    obj_str = obj_io.getvalue()

    obj2_io = StringIO(obj_str)
    unpickler = pickle.Unpickler(obj2_io)
    obj2 = unpickler.load()

    assert obj2() == 578

