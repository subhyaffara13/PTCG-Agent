
def load_onnx_graph(fname):
    import onnx
    m = onnx.load(fname)  # type: ignore[attr-defined]
    g = m.graph
    return parse(g)

