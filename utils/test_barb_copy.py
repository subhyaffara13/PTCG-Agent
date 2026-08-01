
def test_barb_copy():
    fig, ax = plt.subplots()
    u = np.array([1.1])
    v = np.array([2.2])
    b0 = ax.barbs([1], [1], u, v)
    u[0] = 0
    assert b0.u[0] == 1.1
    v[0] = 0
    assert b0.v[0] == 2.2

