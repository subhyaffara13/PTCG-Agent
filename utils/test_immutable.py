
def test_immutable():
    assert not hasattr(b1, '__dict__')
    with raises(AttributeError):
        b1.x = 1


def test_immutable(kdtree_type):
    rng = np.random.RandomState(3965682946)
    n = 1000
    k = 2
    points = rng.rand(n, k)
    T = kdtree_type(points, boxsize=1)
    object_attrs = {
        'm': 3,
        'n': 3,
        'size': 100,
        'leafsize': 12,
        'tree': None,
    }
    for attr, attr_val in object_attrs.items():
        with pytest.raises(AttributeError, match="(is not writable|has no setter)"):
            setattr(T, attr, attr_val)
    array_attrs = {
        'data': np.array([0, 0], dtype=np.float64),
        'indices': 7,
        'boxsize': 4,
        'maxes': 1.5,
        'mins': 1.5,
    }
    for attr, attr_val in array_attrs.items():
        with pytest.raises(ValueError, match="destination is read-only"):
            getattr(T, attr)[:] = attr_val

