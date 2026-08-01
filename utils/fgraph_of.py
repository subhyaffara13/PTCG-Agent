
def fgraph_of(*exprs):
    """ Transform SymPy expressions into Aesara Computation.

    Parameters
    ==========
    exprs
        SymPy expressions

    Returns
    =======
    aesara.graph.fg.FunctionGraph
    """
    outs = list(map(aesara_code_, exprs))
    ins = list(aesara.graph.basic.graph_inputs(outs))
    ins, outs = aesara.graph.basic.clone(ins, outs)
    return aesara.graph.fg.FunctionGraph(ins, outs)


def fgraph_of(*exprs):
    """ Transform SymPy expressions into Theano Computation.

    Parameters
    ==========
    exprs
        SymPy expressions

    Returns
    =======
    theano.gof.FunctionGraph
    """
    outs = list(map(theano_code_, exprs))
    ins = theano.gof.graph.inputs(outs)
    ins, outs = theano.gof.graph.clone(ins, outs)
    return theano.gof.FunctionGraph(ins, outs)

