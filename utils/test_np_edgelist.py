
def test_np_edgelist():
    # see issue #4129
    nx.draw_networkx(barbell, edgelist=np.array([(0, 2), (0, 3)]))

