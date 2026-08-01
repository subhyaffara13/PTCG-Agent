
def test_fill_between_poly_collection_set_data(fig_test, fig_ref, kwargs):
    t = np.linspace(0, 16)
    f1 = np.sin(t)
    f2 = f1 + 0.2

    fig_ref.subplots().fill_between(t, f1, f2, **kwargs)

    coll = fig_test.subplots().fill_between(t, -1, 1.2, **kwargs)
    coll.set_data(t, f1, f2)

