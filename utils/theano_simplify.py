
def theano_simplify(fgraph):
    """ Simplify a Theano Computation.

    Parameters
    ==========
    fgraph : theano.gof.FunctionGraph

    Returns
    =======
    theano.gof.FunctionGraph
    """
    mode = theano.compile.get_default_mode().excluding("fusion")
    fgraph = fgraph.clone()
    mode.optimizer.optimize(fgraph)
    return fgraph

