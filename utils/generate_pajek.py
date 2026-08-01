
def generate_pajek(G):
    """Generate lines in Pajek graph format.

    Parameters
    ----------
    G : graph
       A Networkx graph

    References
    ----------
    See http://vlado.fmf.uni-lj.si/pub/networks/pajek/doc/draweps.htm
    for format information.
    """
    if G.name == "":
        name = "NetworkX"
    else:
        name = G.name
    # Apparently many Pajek format readers can't process this line
    # So we'll leave it out for now.
    # yield '*network %s'%name

    # write nodes with attributes
    yield f"*vertices {G.order()}"
    nodes = list(G)
    # make dictionary mapping nodes to integers
    nodenumber = dict(zip(nodes, range(1, len(nodes) + 1)))
    for n in nodes:
        # copy node attributes and pop mandatory attributes
        # to avoid duplication.
        na = G.nodes.get(n, {}).copy()
        x = na.pop("x", 0.0)
        y = na.pop("y", 0.0)
        try:
            id = int(na.pop("id", nodenumber[n]))
        except ValueError as err:
            err.args += (
                (
                    "Pajek format requires 'id' to be an int()."
                    " Refer to the 'Relabeling nodes' section."
                ),
            )
            raise
        nodenumber[n] = id
        shape = na.pop("shape", "ellipse")
        s = " ".join(map(make_qstr, (id, n, x, y, shape)))
        # only optional attributes are left in na.
        for k, v in na.items():
            if isinstance(v, str) and v.strip() != "":
                s += f" {make_qstr(k)} {make_qstr(v)}"
            else:
                warnings.warn(
                    f"Node attribute {k} is not processed. {('Empty attribute' if isinstance(v, str) else 'Non-string attribute')}."
                )
        yield s

    # write edges with attributes
    if G.is_directed():
        yield "*arcs"
    else:
        yield "*edges"
    for u, v, edgedata in G.edges(data=True):
        d = edgedata.copy()
        value = d.pop("weight", 1.0)  # use 1 as default edge value
        s = " ".join(map(make_qstr, (nodenumber[u], nodenumber[v], value)))
        for k, v in d.items():
            if isinstance(v, str) and v.strip() != "":
                s += f" {make_qstr(k)} {make_qstr(v)}"
            else:
                warnings.warn(
                    f"Edge attribute {k} is not processed. {('Empty attribute' if isinstance(v, str) else 'Non-string attribute')}."
                )
        yield s

