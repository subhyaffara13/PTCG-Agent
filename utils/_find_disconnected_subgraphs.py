
def _find_disconnected_subgraphs(inputs: List[FrozenSet[int]], output: FrozenSet[int]) -> List[FrozenSet[int]]:
    """Finds disconnected subgraphs in the given list of inputs. Inputs are
    connected if they share summation indices. Note: Disconnected subgraphs
    can be contracted independently before forming outer products.

    Parameters:
        inputs: List of sets that represent the lhs side of the einsum subscript
        output: Set that represents the rhs side of the overall einsum subscript

    Returns:
        subgraphs: List containing sets of indices for each subgraph

    Examples:
        ```python
        _find_disconnected_subgraphs([set("ab"), set("c"), set("ad")], set("bd"))
        #> [{0, 2}, {1}]

        _find_disconnected_subgraphs([set("ab"), set("c"), set("ad")], set("abd"))
        #> [{0}, {1}, {2}]
        ```
    """
    subgraphs = []
    unused_inputs = set(range(len(inputs)))

    i_sum = frozenset.union(*inputs) - output  # all summation indices

    while len(unused_inputs) > 0:
        g = set()
        q = [unused_inputs.pop()]
        while len(q) > 0:
            j = q.pop()
            g.add(j)
            i_tmp = i_sum & inputs[j]
            n = {k for k in unused_inputs if len(i_tmp & inputs[k]) > 0}
            q.extend(n)
            unused_inputs.difference_update(n)

        subgraphs.append(g)

    return [frozenset(x) for x in subgraphs]

