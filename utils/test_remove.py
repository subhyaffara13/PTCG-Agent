
def test_remove():
    r = remove(iseven, range(5))
    assert type(r) is not list
    assert list(r) == list(filter(isodd, range(5)))


def test_remove():
    raises(ValueError, lambda: remove(1, 1))
    assert remove(0, 3) == (0, 0)
    for f in range(2, 10):
        for y in range(2, 1000):
            for z in [1, 17, 101, 1009]:
                assert remove(z*f**y, f) == (z, y)


def test_remove(temp_hdfstore):
    store = temp_hdfstore
    ts = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    store["a"] = ts
    store["b"] = df
    store.remove("a")
    assert len(store) == 1
    tm.assert_frame_equal(df, store["b"])

    store.remove("b")
    assert len(store) == 0

    # nonexistence
    with pytest.raises(
        KeyError, match="'No object named a_nonexistent_store in the file'"
    ):
        store.remove("a_nonexistent_store")

    # pathing
    store["a"] = ts
    store["b/foo"] = df
    store.remove("b/foo")
    assert len(store) == 1

    store["a"] = ts
    store["b/foo"] = df
    store.remove("b")
    assert len(store) == 1

    # __delitem__
    store["a"] = ts
    store["b"] = df
    del store["a"]
    del store["b"]
    assert len(store) == 0


def test_remove():
    fig, ax = plt.subplots()
    im = ax.imshow(np.arange(36).reshape(6, 6))
    ln, = ax.plot(range(5))

    assert fig.stale
    assert ax.stale

    fig.canvas.draw()
    assert not fig.stale
    assert not ax.stale
    assert not ln.stale

    assert im in ax._mouseover_set
    assert ln not in ax._mouseover_set
    assert im.axes is ax

    im.remove()
    ln.remove()

    for art in [im, ln]:
        assert art.axes is None
        assert art.get_figure() is None

    assert im not in ax._mouseover_set
    assert fig.stale
    assert ax.stale

