
def test_quiver_key_memory_leak():
    fig, ax = plt.subplots()

    Q = draw_quiver(ax)

    qk = ax.quiverkey(Q, 0.5, 0.92, 2, r'$2 \frac{m}{s}$',
                      labelpos='W',
                      fontproperties={'weight': 'bold'})
    orig_refcount = sys.getrefcount(qk)
    qk.remove()
    assert sys.getrefcount(qk) < orig_refcount

