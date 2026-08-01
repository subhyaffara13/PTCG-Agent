
def greedy(
    inputs: List[ArrayIndexType],
    output: ArrayIndexType,
    size_dict: Dict[str, int],
    memory_limit: Optional[int] = None,
    choose_fn: Any = None,
    cost_fn: str = "memory-removed",
) -> PathType:
    """Finds the path by a three stage algorithm:

    1. Eagerly compute Hadamard products.
    2. Greedily compute contractions to maximize `removed_size`
    3. Greedily compute outer products.

    This algorithm scales quadratically with respect to the
    maximum number of elements sharing a common dim.

    Parameters:
        inputs: List of sets that represent the lhs side of the einsum subscript
        output: Set that represents the rhs side of the overall einsum subscript
        size_dict: Dictionary of index sizes
        memory_limit: The maximum number of elements in a temporary array
        choose_fn: A function that chooses which contraction to perform from the queue
        cost_fn: A function that assigns a potential contraction a cost.

    Returns:
        path: The contraction order (a list of tuples of ints).

    Examples:
        ```python
        isets = [set('abd'), set('ac'), set('bdc')]
        oset = set('')
        idx_sizes = {'a': 1, 'b':2, 'c':3, 'd':4}
        greedy(isets, oset, idx_sizes)
        #> [(0, 2), (0, 1)]
        ```
    """
    if memory_limit not in _UNLIMITED_MEM:
        return branch(inputs, output, size_dict, memory_limit, nbranch=1, cost_fn=cost_fn)  # type: ignore

    ssa_path = ssa_greedy_optimize(inputs, output, size_dict, cost_fn=cost_fn, choose_fn=choose_fn)
    return ssa_to_linear(ssa_path)


def greedy(tree, objective=identity, **kwargs):
    """ Execute a strategic tree.  Select alternatives greedily

    Trees
    -----

    Nodes in a tree can be either

    function - a leaf
    list     - a selection among operations
    tuple    - a sequence of chained operations

    Textual examples
    ----------------

    Text: Run f, then run g, e.g. ``lambda x: g(f(x))``
    Code: ``(f, g)``

    Text: Run either f or g, whichever minimizes the objective
    Code: ``[f, g]``

    Textx: Run either f or g, whichever is better, then run h
    Code: ``([f, g], h)``

    Text: Either expand then simplify or try factor then foosimp. Finally print
    Code: ``([(expand, simplify), (factor, foosimp)], print)``

    Objective
    ---------

    "Better" is determined by the objective keyword.  This function makes
    choices to minimize the objective.  It defaults to the identity.

    Examples
    ========

    >>> from sympy.strategies.tree import greedy
    >>> inc    = lambda x: x + 1
    >>> dec    = lambda x: x - 1
    >>> double = lambda x: 2*x

    >>> tree = [inc, (dec, double)] # either inc or dec-then-double
    >>> fn = greedy(tree)
    >>> fn(4)  # lowest value comes from the inc
    5
    >>> fn(1)  # lowest value comes from dec then double
    0

    This function selects between options in a tuple.  The result is chosen
    that minimizes the objective function.

    >>> fn = greedy(tree, objective=lambda x: -x)  # maximize
    >>> fn(4)  # highest value comes from the dec then double
    6
    >>> fn(1)  # highest value comes from the inc
    2

    Greediness
    ----------

    This is a greedy algorithm.  In the example:

        ([a, b], c)  # do either a or b, then do c

    the choice between running ``a`` or ``b`` is made without foresight to c
    """
    optimize = partial(minimize, objective=objective)
    return treeapply(tree, {list: optimize, tuple: chain}, **kwargs)

