
def test_vertex_markers():
    data = list(range(10))
    marker_as_tuple = ((-1, -1), (1, -1), (1, 1), (-1, 1))
    marker_as_list = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    fig, ax = plt.subplots()
    ax.plot(data, linestyle='', marker=marker_as_tuple, mfc='k')
    ax.plot(data[::-1], linestyle='', marker=marker_as_list, mfc='b')
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)

