
def test_vertexselector():
    line, = plt.plot([0, 1], picker=True)
    pickle.loads(pickle.dumps(VertexSelector(line)))

