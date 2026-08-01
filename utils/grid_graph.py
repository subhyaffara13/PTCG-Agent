
def grid_graph(dim, periodic=False):
    """Returns the *n*-dimensional grid graph.

    The dimension *n* is the length of the list `dim` and the size in
    each dimension is the value of the corresponding list element.

    Parameters
    ----------
    dim : list or tuple of numbers or iterables of nodes
        'dim' is a tuple or list with, for each dimension, either a number
        that is the size of that dimension or an iterable of nodes for
        that dimension. The dimension of the grid_graph is the length
        of `dim`.

    periodic : bool or iterable
        If `periodic` is True, all dimensions are periodic. If False all
        dimensions are not periodic. If `periodic` is iterable, it should
        yield `dim` bool values each of which indicates whether the
        corresponding axis is periodic.

    Returns
    -------
    NetworkX graph
        The (possibly periodic) grid graph of the specified dimensions.

    See Also
    --------
    grid_2d_graph, triangular_lattice_graph, hexagonal_lattice_graph :
        2D lattice graphs
    hypercube_graph :
        A special case of `grid_graph` where all elements of `dim` are identical

    Examples
    --------
    To produce a 2 by 3 by 4 grid graph, a graph on 24 nodes:

    >>> from networkx import grid_graph
    >>> G = grid_graph(dim=(2, 3, 4))
    >>> len(G)
    24
    >>> G = grid_graph(dim=(range(7, 9), range(3, 6)))
    >>> len(G)
    6
    """
    from collections.abc import Iterable

    from networkx.algorithms.operators.product import cartesian_product

    if not dim:
        return empty_graph(0)

    periodic = repeat(periodic) if not isinstance(periodic, Iterable) else periodic
    func = (cycle_graph if p else path_graph for p in periodic)

    G = next(func)(dim[0])
    for current_dim in dim[1:]:
        Gnew = next(func)(current_dim)
        G = cartesian_product(Gnew, G)
    # graph G is done but has labels of the form (1, (2, (3, 1))) so relabel
    H = relabel_nodes(G, flatten)
    return H

