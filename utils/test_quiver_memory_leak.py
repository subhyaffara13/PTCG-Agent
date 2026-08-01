
def test_quiver_memory_leak():
    fig, ax = plt.subplots()

    Q = draw_quiver(ax)
    ttX = Q.X
    orig_refcount = sys.getrefcount(ttX)
    Q.remove()

    del Q

    assert sys.getrefcount(ttX) < orig_refcount

