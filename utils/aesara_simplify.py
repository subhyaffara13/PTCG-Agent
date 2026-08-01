
def aesara_simplify(fgraph):
    """ Simplify a Aesara Computation.

    Parameters
    ==========
    fgraph : aesara.graph.fg.FunctionGraph

    Returns
    =======
    aesara.graph.fg.FunctionGraph
    """
    mode = aesara.compile.get_default_mode().excluding("fusion")
    fgraph = fgraph.clone()
    mode.optimizer.rewrite(fgraph)
    return fgraph

