
def test_quiver_copy():
    fig, ax = plt.subplots()
    uv = dict(u=np.array([1.1]), v=np.array([2.0]))
    q0 = ax.quiver([1], [1], uv['u'], uv['v'])
    uv['v'][0] = 0
    assert q0.V[0] == 2.0

