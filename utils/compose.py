
def compose(*funcs):
    """ Compose functions to operate in series.

    Returns a function that applies other functions in sequence.

    Functions are applied from right to left so that
    ``compose(f, g, h)(x, y)`` is the same as ``f(g(h(x, y)))``.

    If no arguments are provided, the identity function (f(x) = x) is returned.

    >>> inc = lambda i: i + 1
    >>> compose(str, inc)(3)
    '4'

    See Also:
        compose_left
        pipe
    """
    if not funcs:
        return identity
    if len(funcs) == 1:
        return funcs[0]
    else:
        return Compose(funcs)


def compose(stream, Loader=Loader):
    """
    Parse the first YAML document in a stream
    and produce the corresponding representation tree.
    """
    loader = Loader(stream)
    try:
        return loader.get_single_node()
    finally:
        loader.dispose()


def compose(*funcs):
    def compose_two(f1, f2):
        return lambda *args, **kwargs: f1(f2(*args, **kwargs))

    return functools.reduce(compose_two, funcs)


def compose(f, g, *gens, **args):
    """
    Compute functional composition ``f(g)``.

    Examples
    ========

    >>> from sympy import compose
    >>> from sympy.abc import x

    >>> compose(x**2 + x, x - 1)
    x**2 - x

    """
    options.allowed_flags(args, ['polys'])

    try:
        (F, G), opt = parallel_poly_from_expr((f, g), *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('compose', 2, exc)

    result = F.compose(G)

    if not opt.polys:
        return result.as_expr()
    else:
        return result


def compose(*funcs):
    def compose_two(f1, f2):
        return lambda *args, **kwargs: f1(f2(*args, **kwargs))

    return functools.reduce(compose_two, funcs)


def compose(*funcs):
    """
    Compose any number of unary functions into a single unary function.

    Comparable to
    `function composition <https://en.wikipedia.org/wiki/Function_composition>`_
    in mathematics:

    ``h = g ∘ f`` implies ``h(x) = g(f(x))``.

    In Python, ``h = compose(g, f)``.

    >>> import textwrap
    >>> expected = str.strip(textwrap.dedent(compose.__doc__))
    >>> strip_and_dedent = compose(str.strip, textwrap.dedent)
    >>> strip_and_dedent(compose.__doc__) == expected
    True

    Compose also allows the innermost function to take arbitrary arguments.

    >>> round_three = lambda x: round(x, ndigits=3)
    >>> f = compose(round_three, int.__truediv__)
    >>> [f(3*x, x+1) for x in range(1,10)]
    [1.5, 2.0, 2.25, 2.4, 2.5, 2.571, 2.625, 2.667, 2.7]
    """

    def compose_two(f1, f2):
        return lambda *args, **kwargs: f1(f2(*args, **kwargs))

    return functools.reduce(compose_two, funcs)


def compose(G, H):
    """Compose graph G with H by combining nodes and edges into a single graph.

    The node sets and edges sets do not need to be disjoint.

    Composing preserves the attributes of nodes and edges.
    Attribute values from H take precedent over attribute values from G.

    Parameters
    ----------
    G, H : graph
       A NetworkX graph

    Returns
    -------
    C: A new graph with the same type as G

    See Also
    --------
    :func:`~networkx.Graph.update`
    union
    disjoint_union

    Notes
    -----
    It is recommended that G and H be either both directed or both undirected.

    For MultiGraphs, the edges are identified by incident nodes AND edge-key.
    This can cause surprises (i.e., edge `(1, 2)` may or may not be the same
    in two graphs) if you use MultiGraph without keeping track of edge keys.

    If combining the attributes of common nodes is not desired, consider union(),
    which raises an exception for name collisions.

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2)])
    >>> H = nx.Graph([(0, 1), (1, 2)])
    >>> R = nx.compose(G, H)
    >>> R.nodes
    NodeView((0, 1, 2))
    >>> R.edges
    EdgeView([(0, 1), (0, 2), (1, 2)])

    By default, the attributes from `H` take precedent over attributes from `G`.
    If you prefer another way of combining attributes, you can update them after the compose operation:

    >>> G = nx.Graph([(0, 1, {"weight": 2.0}), (3, 0, {"weight": 100.0})])
    >>> H = nx.Graph([(0, 1, {"weight": 10.0}), (1, 2, {"weight": -1.0})])
    >>> nx.set_node_attributes(G, {0: "dark", 1: "light", 3: "black"}, name="color")
    >>> nx.set_node_attributes(H, {0: "green", 1: "orange", 2: "yellow"}, name="color")
    >>> GcomposeH = nx.compose(G, H)

    Normally, color attribute values of nodes of GcomposeH come from H. We can workaround this as follows:

    >>> node_data = {
    ...     n: G.nodes[n]["color"] + " " + H.nodes[n]["color"]
    ...     for n in G.nodes & H.nodes
    ... }
    >>> nx.set_node_attributes(GcomposeH, node_data, "color")
    >>> print(GcomposeH.nodes[0]["color"])
    dark green

    >>> print(GcomposeH.nodes[3]["color"])
    black

    Similarly, we can update edge attributes after the compose operation in a way we prefer:

    >>> edge_data = {
    ...     e: G.edges[e]["weight"] * H.edges[e]["weight"] for e in G.edges & H.edges
    ... }
    >>> nx.set_edge_attributes(GcomposeH, edge_data, "weight")
    >>> print(GcomposeH.edges[(0, 1)]["weight"])
    20.0

    >>> print(GcomposeH.edges[(3, 0)]["weight"])
    100.0
    """
    return nx.compose_all([G, H])

