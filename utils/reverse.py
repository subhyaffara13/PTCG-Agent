
def reverse(G, copy=True):
    """Returns the reverse directed graph of G.

    Parameters
    ----------
    G : directed graph
        A NetworkX directed graph
    copy : bool
        If True, then a new graph is returned. If False, then the graph is
        reversed in place.

    Returns
    -------
    H : directed graph
        The reversed G.

    Raises
    ------
    NetworkXError
        If graph is undirected.

    Examples
    --------
    >>> G = nx.DiGraph([(1, 2), (1, 3), (2, 3), (3, 4), (3, 5)])
    >>> G_reversed = nx.reverse(G)
    >>> G_reversed.edges()
    OutEdgeView([(2, 1), (3, 1), (3, 2), (4, 3), (5, 3)])

    """
    if not G.is_directed():
        raise nx.NetworkXError("Cannot reverse an undirected graph.")
    else:
        return G.reverse(copy=copy)


def reverse(operand: _ods_ir.Value[_ods_ir.RankedTensorType], dimensions: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ReverseOp(operand=operand, dimensions=dimensions, results=results, loc=loc, ip=ip).result


def reverse(operand: _ods_ir.Value[_ods_ir.RankedTensorType], dimensions: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ReverseOp(operand=operand, dimensions=dimensions, results=results, loc=loc, ip=ip).result

