
def read_graph(name):
    fname = (
        importlib.resources.files("networkx.algorithms.flow.tests")
        / f"{name}.gpickle.bz2"
    )

    with bz2.BZ2File(fname, "rb") as f:
        G = pickle.load(f)
    return G

