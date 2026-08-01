
def test_fill_between_poly_collection_raise(t_direction, f1, shape, where, msg):
    t = np.linspace(0, 16)
    f1 = np.sin(t) if f1 is None else np.asarray(f1)
    f2 = f1 + 0.2
    if shape:
        t = t.reshape(*shape)
    with pytest.raises(ValueError, match=msg):
        FillBetweenPolyCollection(t_direction, t, f1, f2, where=where)

