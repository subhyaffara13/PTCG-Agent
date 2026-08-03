from typing import Any, Dict, Optional, Tuple, Union

def contract_path(
    subscripts: str,
    *operands: ArrayType,
    use_blas: bool = True,
    optimize: OptimizeKind = True,
    memory_limit: _MemoryLimit = None,
    shapes: bool = False,
    **kwargs: Any,
) -> Tuple[PathType, PathInfo]: ...


def contract_path(
    subscripts: ArrayType,
    *operands: Union[ArrayType, Collection[int]],
    use_blas: bool = True,
    optimize: OptimizeKind = True,
    memory_limit: _MemoryLimit = None,
    shapes: bool = False,
    **kwargs: Any,
) -> Tuple[PathType, PathInfo]: ...


def contract_path(
    subscripts: Any,
    *operands: Any,
    use_blas: bool = True,
    optimize: OptimizeKind = True,
    memory_limit: _MemoryLimit = None,
    shapes: bool = False,
    **kwargs: Any,
) -> Tuple[PathType, PathInfo]:
    """Find a contraction order `path`, without performing the contraction.

    Parameters:
          subscripts: Specifies the subscripts for summation.
          *operands: These are the arrays for the operation.
          use_blas: Do you use BLAS for valid operations, may use extra memory for more intermediates.
          optimize: Choose the type of path the contraction will be optimized with.
                - if a list is given uses this as the path.
                - `'optimal'` An algorithm that explores all possible ways of
                contracting the listed tensors. Scales factorially with the number of
                terms in the contraction.
                - `'dp'` A faster (but essentially optimal) algorithm that uses
                dynamic programming to exhaustively search all contraction paths
                without outer-products.
                - `'greedy'` An cheap algorithm that heuristically chooses the best
                pairwise contraction at each step. Scales linearly in the number of
                terms in the contraction.
                - `'random-greedy'` Run a randomized version of the greedy algorithm
                32 times and pick the best path.
                - `'random-greedy-128'` Run a randomized version of the greedy
                algorithm 128 times and pick the best path.
                - `'branch-all'` An algorithm like optimal but that restricts itself
                to searching 'likely' paths. Still scales factorially.
                - `'branch-2'` An even more restricted version of 'branch-all' that
                only searches the best two options at each step. Scales exponentially
                with the number of terms in the contraction.
                - `'auto'` Choose the best of the above algorithms whilst aiming to
                keep the path finding time below 1ms.
                - `'auto-hq'` Aim for a high quality contraction, choosing the best
                of the above algorithms whilst aiming to keep the path finding time
                below 1sec.

          memory_limit: Give the upper bound of the largest intermediate tensor contract will build.
                - None or -1 means there is no limit
                - `max_input` means the limit is set as largest input tensor
                - a positive integer is taken as an explicit limit on the number of elements

                The default is None. Note that imposing a limit can make contractions
                exponentially slower to perform.

          shapes: Whether ``contract_path`` should assume arrays (the default) or array shapes have been supplied.

    Returns:
          path: The optimized einsum contraciton path
          PathInfo: A printable object containing various information about the path found.

    Notes:
          The resulting path indicates which terms of the input contraction should be
          contracted first, the result of this contraction is then appended to the end of
          the contraction list.

    Examples:
          We can begin with a chain dot example. In this case, it is optimal to
          contract the b and c tensors represented by the first element of the path (1,
          2). The resulting tensor is added to the end of the contraction and the
          remaining contraction, `(0, 1)`, is then executed.

      ```python
      a = np.random.rand(2, 2)
      b = np.random.rand(2, 5)
      c = np.random.rand(5, 2)
      path_info = opt_einsum.contract_path('ij,jk,kl->il', a, b, c)
      print(path_info[0])
      #> [(1, 2), (0, 1)]
      print(path_info[1])
      #>   Complete contraction:  ij,jk,kl->il
      #>          Naive scaling:  4
      #>      Optimized scaling:  3
      #>       Naive FLOP count:  1.600e+02
      #>   Optimized FLOP count:  5.600e+01
      #>    Theoretical speedup:  2.857
      #>   Largest intermediate:  4.000e+00 elements
      #> -------------------------------------------------------------------------
      #> scaling                  current                                remaining
      #> -------------------------------------------------------------------------
      #>    3                   kl,jk->jl                                ij,jl->il
      #>    3                   jl,ij->il                                   il->il
      ```

      A more complex index transformation example.

      ```python
      I = np.random.rand(10, 10, 10, 10)
      C = np.random.rand(10, 10)
      path_info = oe.contract_path('ea,fb,abcd,gc,hd->efgh', C, C, I, C, C)

      print(path_info[0])
      #> [(0, 2), (0, 3), (0, 2), (0, 1)]
      print(path_info[1])
      #>   Complete contraction:  ea,fb,abcd,gc,hd->efgh
      #>          Naive scaling:  8
      #>      Optimized scaling:  5
      #>       Naive FLOP count:  8.000e+08
      #>   Optimized FLOP count:  8.000e+05
      #>    Theoretical speedup:  1000.000
      #>   Largest intermediate:  1.000e+04 elements
      #> --------------------------------------------------------------------------
      #> scaling                  current                                remaining
      #> --------------------------------------------------------------------------
      #>    5               abcd,ea->bcde                      fb,gc,hd,bcde->efgh
      #>    5               bcde,fb->cdef                         gc,hd,cdef->efgh
      #>    5               cdef,gc->defg                            hd,defg->efgh
      #>    5               defg,hd->efgh                               efgh->efgh
      ```
    """
    if (optimize is True) or (optimize is None):
        optimize = "auto"

    # Hidden option, only einsum should call this
    einsum_call_arg = kwargs.pop("einsum_call", False)
    if len(kwargs):
        raise TypeError(f"Did not understand the following kwargs: {kwargs.keys()}")

    # Python side parsing
    operands_ = [subscripts] + list(operands)
    input_subscripts, output_subscript, operands_prepped = parser.parse_einsum_input(operands_, shapes=shapes)

    # Build a few useful list and sets
    input_list = input_subscripts.split(",")
    input_sets = [frozenset(x) for x in input_list]
    if shapes:
        input_shapes = operands_prepped
    else:
        input_shapes = [parser.get_shape(x) for x in operands_prepped]
    output_set = frozenset(output_subscript)
    indices = frozenset(input_subscripts.replace(",", ""))

    # Get length of each unique dimension and ensure all dimensions are correct
    size_dict: Dict[str, int] = {}
    for tnum, term in enumerate(input_list):
        sh = input_shapes[tnum]

        if len(sh) != len(term):
            raise ValueError(
                f"Einstein sum subscript '{input_list[tnum]}' does not contain the "
                f"correct number of indices for operand {tnum}."
            )
        for cnum, char in enumerate(term):
            dim = int(sh[cnum])

            if char in size_dict:
                # For broadcasting cases we always want the largest dim size
                if size_dict[char] == 1:
                    size_dict[char] = dim
                elif dim not in (1, size_dict[char]):
                    raise ValueError(
                        f"Size of label '{char}' for operand {tnum} ({size_dict[char]}) does not match previous "
                        f"terms ({dim})."
                    )
            else:
                size_dict[char] = dim

    # Compute size of each input array plus the output array
    size_list = [helpers.compute_size_by_dict(term, size_dict) for term in input_list + [output_subscript]]
    memory_arg = _choose_memory_arg(memory_limit, size_list)

    num_ops = len(input_list)

    # Compute naive cost
    # This is not quite right, need to look into exactly how einsum does this
    # indices_in_input = input_subscripts.replace(',', '')
    inner_product = (sum(len(x) for x in input_sets) - len(indices)) > 0
    naive_cost = helpers.flop_count(indices, inner_product, num_ops, size_dict)

    # Compute the path
    if optimize is False:
        path_tuple: PathType = [tuple(range(num_ops))]
    elif not isinstance(optimize, (str, paths.PathOptimizer)):
        # Custom path supplied
        path_tuple = optimize  # type: ignore
    elif num_ops <= 2:
        # Nothing to be optimized
        path_tuple = [tuple(range(num_ops))]
    elif isinstance(optimize, paths.PathOptimizer):
        # Custom path optimizer supplied
        path_tuple = optimize(input_sets, output_set, size_dict, memory_arg)
    else:
        path_optimizer = paths.get_path_fn(optimize)
        path_tuple = path_optimizer(input_sets, output_set, size_dict, memory_arg)

    cost_list = []
    scale_list = []
    size_list = []
    contraction_list = []

    # Build contraction tuple (positions, gemm, einsum_str, remaining)
    for cnum, contract_inds in enumerate(path_tuple):
        # Make sure we remove inds from right to left
        contract_inds = tuple(sorted(contract_inds, reverse=True))

        contract_tuple = helpers.find_contraction(contract_inds, input_sets, output_set)
        out_inds, input_sets, idx_removed, idx_contract = contract_tuple

        # Compute cost, scale, and size
        cost = helpers.flop_count(idx_contract, bool(idx_removed), len(contract_inds), size_dict)
        cost_list.append(cost)
        scale_list.append(len(idx_contract))
        size_list.append(helpers.compute_size_by_dict(out_inds, size_dict))

        tmp_inputs = [input_list.pop(x) for x in contract_inds]
        tmp_shapes = [input_shapes.pop(x) for x in contract_inds]

        if use_blas:
            do_blas = blas.can_blas(tmp_inputs, "".join(out_inds), idx_removed, tmp_shapes)
        else:
            do_blas = False

        # Last contraction
        if (cnum - len(path_tuple)) == -1:
            idx_result = output_subscript
        else:
            # use tensordot order to minimize transpositions
            all_input_inds = "".join(tmp_inputs)
            idx_result = "".join(sorted(out_inds, key=all_input_inds.find))

        shp_result = parser.find_output_shape(tmp_inputs, tmp_shapes, idx_result)

        input_list.append(idx_result)
        input_shapes.append(shp_result)

        einsum_str = ",".join(tmp_inputs) + "->" + idx_result

        # for large expressions saving the remaining terms at each step can
        # incur a large memory footprint - and also be messy to print
        if len(input_list) <= 20:
            remaining: Optional[Tuple[str, ...]] = tuple(input_list)
        else:
            remaining = None

        contraction = (contract_inds, idx_removed, einsum_str, remaining, do_blas)
        contraction_list.append(contraction)

    opt_cost = sum(cost_list)

    if einsum_call_arg:
        return operands_prepped, contraction_list  # type: ignore

    path_print = PathInfo(
        contraction_list,
        input_subscripts,
        output_subscript,
        indices,
        path_tuple,
        scale_list,
        naive_cost,
        opt_cost,
        size_list,
        size_dict,
    )

    return path_tuple, path_print

