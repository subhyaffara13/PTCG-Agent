
def to_directed(graph):
    """Returns a directed view of the graph `graph`.

    Identical to graph.to_directed(as_view=True)
    Note that graph.to_directed defaults to `as_view=False`
    while this function always provides a view.
    """
    return graph.to_directed(as_view=True)

