
def einsum_path(*operands, optimize='greedy', einsum_call=False):
    """
    einsum_path(subscripts, *operands, optimize='greedy')

    Evaluates the lowest cost contraction order for an einsum expression by
    considering the creation of intermediate arrays.

    Parameters
    ----------
    subscripts : str
        Specifies the subscripts for summation.
    *operands : list of array_like
        These are the arrays for the operation.
    optimize : {bool, list, tuple, 'greedy', 'optimal'}
        Choose the type of path. If a tuple is provided, the second argument is
        assumed to be the maximum intermediate size created. If only a single
        argument is provided the largest input or output array size is used
        as a maximum intermediate size.

        * if a list is given that starts with ``einsum_path``, uses this as the
          contraction path
        * if False no optimization is taken
        * if True defaults to the 'greedy' algorithm
        * 'optimal' An algorithm that combinatorially explores all possible
          ways of contracting the listed tensors and chooses the least costly
          path. Scales exponentially with the number of terms in the
          contraction.
        * 'greedy' An algorithm that chooses the best pair contraction
          at each step. Effectively, this algorithm searches the largest inner,
          Hadamard, and then outer products at each step. Scales cubically with
          the number of terms in the contraction. Equivalent to the 'optimal'
          path for most contractions.

        Default is 'greedy'.

    Returns
    -------
    path : list of tuples
        A list representation of the einsum path.
    string_repr : str
        A printable representation of the einsum path.

    Notes
    -----
    The resulting path indicates which terms of the input contraction should be
    contracted first, the result of this contraction is then appended to the
    end of the contraction list. This list can then be iterated over until all
    intermediate contractions are complete.

    See Also
    --------
    einsum, linalg.multi_dot

    Examples
    --------

    We can begin with a chain dot example. In this case, it is optimal to
    contract the ``b`` and ``c`` tensors first as represented by the first
    element of the path ``(1, 2)``. The resulting tensor is added to the end
    of the contraction and the remaining contraction ``(0, 1)`` is then
    completed.

    >>> np.random.seed(123)
    >>> a = np.random.rand(2, 2)
    >>> b = np.random.rand(2, 5)
    >>> c = np.random.rand(5, 2)
    >>> path_info = np.einsum_path('ij,jk,kl->il', a, b, c, optimize='greedy')
    >>> print(path_info[0])
    ['einsum_path', (1, 2), (0, 1)]
    >>> print(path_info[1])
      Complete contraction:  ij,jk,kl->il # may vary
             Naive scaling:  4
         Optimized scaling:  3
          Naive FLOP count:  1.600e+02
      Optimized FLOP count:  5.600e+01
       Theoretical speedup:  2.857
      Largest intermediate:  4.000e+00 elements
    -------------------------------------------------------------------------
    scaling                  current                                remaining
    -------------------------------------------------------------------------
       3                   kl,jk->jl                                ij,jl->il
       3                   jl,ij->il                                   il->il


    A more complex index transformation example.

    >>> I = np.random.rand(10, 10, 10, 10)
    >>> C = np.random.rand(10, 10)
    >>> path_info = np.einsum_path('ea,fb,abcd,gc,hd->efgh', C, C, I, C, C,
    ...                            optimize='greedy')

    >>> print(path_info[0])
    ['einsum_path', (0, 2), (0, 3), (0, 2), (0, 1)]
    >>> print(path_info[1])
      Complete contraction:  ea,fb,abcd,gc,hd->efgh # may vary
             Naive scaling:  8
         Optimized scaling:  5
          Naive FLOP count:  8.000e+08
      Optimized FLOP count:  8.000e+05
       Theoretical speedup:  1000.000
      Largest intermediate:  1.000e+04 elements
    --------------------------------------------------------------------------
    scaling                  current                                remaining
    --------------------------------------------------------------------------
       5               abcd,ea->bcde                      fb,gc,hd,bcde->efgh
       5               bcde,fb->cdef                         gc,hd,cdef->efgh
       5               cdef,gc->defg                            hd,defg->efgh
       5               defg,hd->efgh                               efgh->efgh
    """

    # Figure out what the path really is
    path_type = optimize
    if path_type is True:
        path_type = 'greedy'
    if path_type is None:
        path_type = False

    explicit_einsum_path = False
    memory_limit = None

    # No optimization or a named path algorithm
    if (path_type is False) or isinstance(path_type, str):
        pass

    # Given an explicit path
    elif len(path_type) and (path_type[0] == 'einsum_path'):
        explicit_einsum_path = True

    # Path tuple with memory limit
    elif ((len(path_type) == 2) and isinstance(path_type[0], str) and
            isinstance(path_type[1], (int, float))):
        memory_limit = int(path_type[1])
        path_type = path_type[0]

    else:
        raise TypeError(f"Did not understand the path: {str(path_type)}")

    # Hidden option, only einsum should call this
    einsum_call_arg = einsum_call

    # Python side parsing
    input_subscripts, output_subscript, operands = (
        _parse_einsum_input(operands)
    )

    # Build a few useful list and sets
    input_list = input_subscripts.split(',')
    num_inputs = len(input_list)
    input_sets = [set(x) for x in input_list]
    output_set = set(output_subscript)
    indices = set(input_subscripts.replace(',', ''))
    num_indices = len(indices)

    # Get length of each unique dimension and ensure all dimensions are correct
    dimension_dict = {}
    for tnum, term in enumerate(input_list):
        sh = operands[tnum].shape
        if len(sh) != len(term):
            raise ValueError(f"Einstein sum subscript {input_subscripts[tnum]} "
                             "does not contain the "
                             f"correct number of indices for operand {tnum}.")
        for cnum, char in enumerate(term):
            dim = sh[cnum]

            if char in dimension_dict.keys():
                # For broadcasting cases we always want the largest dim size
                if dimension_dict[char] == 1:
                    dimension_dict[char] = dim
                elif dim not in (1, dimension_dict[char]):
                    raise ValueError(f"Size of label {char!r} for "
                                     f"operand {tnum} ({dimension_dict[char]}) "
                                     f"does not match previous terms ({dim}).")
            else:
                dimension_dict[char] = dim

    # Compute size of each input array plus the output array
    size_list = [_compute_size_by_dict(term, dimension_dict)
                 for term in input_list + [output_subscript]]
    max_size = max(size_list)

    if memory_limit is None:
        memory_arg = max_size
    else:
        memory_arg = memory_limit

    # Compute the path
    if explicit_einsum_path:
        path = path_type[1:]
    elif (
        (path_type is False)
        or (num_inputs in [1, 2])
        or (indices == output_set)
    ):
        # Nothing to be optimized, leave it to einsum
        path = [tuple(range(num_inputs))]
    elif path_type == "greedy":
        path = _greedy_path(
            input_sets, output_set, dimension_dict, memory_arg
        )
    elif path_type == "optimal":
        path = _optimal_path(
            input_sets, output_set, dimension_dict, memory_arg
        )
    else:
        raise KeyError("Path name %s not found", path_type)

    cost_list, scale_list, size_list, contraction_list = [], [], [], []

    # Build contraction tuple (positions, gemm, einsum_str, remaining)
    for cnum, contract_inds in enumerate(path):
        # Make sure we remove inds from right to left
        contract_inds = tuple(sorted(contract_inds, reverse=True))

        contract = _find_contraction(contract_inds, input_sets, output_set)
        out_inds, input_sets, idx_removed, idx_contract = contract

        if not einsum_call_arg:
            # these are only needed for printing info
            cost = _flop_count(
                idx_contract, idx_removed, len(contract_inds), dimension_dict
            )
            cost_list.append(cost)
            scale_list.append(len(idx_contract))
            size_list.append(_compute_size_by_dict(out_inds, dimension_dict))

        tmp_inputs = []
        for x in contract_inds:
            tmp_inputs.append(input_list.pop(x))

        # Last contraction
        if (cnum - len(path)) == -1:
            idx_result = output_subscript
        else:
            sort_result = [(dimension_dict[ind], ind) for ind in out_inds]
            idx_result = "".join([x[1] for x in sorted(sort_result)])

        input_list.append(idx_result)
        einsum_str = ",".join(tmp_inputs) + "->" + idx_result

        contraction = (contract_inds, einsum_str, input_list[:])
        contraction_list.append(contraction)

    if len(input_list) != 1:
        # Explicit "einsum_path" is usually trusted, but we detect this kind of
        # mistake in order to prevent from returning an intermediate value.
        raise RuntimeError(
            f"Invalid einsum_path is specified: {len(input_list) - 1} more "
            "operands has to be contracted.")

    if einsum_call_arg:
        return (operands, contraction_list)

    # Return the path along with a nice string representation
    overall_contraction = input_subscripts + "->" + output_subscript

    # Compute naive cost
    # This isn't quite right, need to look into exactly how einsum does this
    inner_product = (
        sum(len(set(x)) for x in input_subscripts.split(',')) - num_indices
    ) > 0
    naive_cost = _flop_count(
        indices, inner_product, num_inputs, dimension_dict
    )

    opt_cost = sum(cost_list) + 1
    speedup = naive_cost / opt_cost
    max_i = max(size_list)

    path_print = f"  Complete contraction:  {overall_contraction}\n"
    path_print += f"         Naive scaling:  {num_indices}\n"
    path_print += f"     Optimized scaling:  {max(scale_list)}\n"
    path_print += f"      Naive FLOP count:  {naive_cost:.3e}\n"
    path_print += f"  Optimized FLOP count:  {opt_cost:.3e}\n"
    path_print += f"   Theoretical speedup:  {speedup:3.3f}\n"
    path_print += f"  Largest intermediate:  {max_i:.3e} elements\n"
    path_print += "-" * 74 + "\n"
    path_print += f"{'scaling':>6} {'current':>24} {'remaining':>40}\n"
    path_print += "-" * 74

    for n, contraction in enumerate(contraction_list):
        _, einsum_str, remaining = contraction
        remaining_str = ",".join(remaining) + "->" + output_subscript
        path_print += f"\n{scale_list[n]:4d}    {einsum_str:>24} {remaining_str:>40}"

    path = ['einsum_path'] + path
    return (path, path_print)


def einsum_path(
    subscripts: str, /,
    *operands: ArrayLike,
    optimize: bool | str | list[tuple[int, ...]] =  ...,
) -> tuple[list[tuple[int, ...]], Any]: ...


def einsum_path(
    arr: ArrayLike,
    axes: Sequence[Any], /,
    *operands: ArrayLike | Sequence[Any],
    optimize: bool | str | list[tuple[int, ...]] =  ...,
) -> tuple[list[tuple[int, ...]], Any]: ...


def einsum_path(
    subscripts, /,
    *operands,
    optimize: bool | str | list[tuple[int, ...]] = 'auto'
  ) -> tuple[list[tuple[int, ...]], Any]:
  """Evaluates the optimal contraction path without evaluating the einsum.

  JAX implementation of :func:`numpy.einsum_path`. This function calls into
  the opt_einsum_ package, and makes use of its optimization routines.

  Args:
    subscripts: string containing axes names separated by commas.
    *operands: sequence of one or more arrays corresponding to the subscripts.
    optimize: specify how to optimize the order of computation. In JAX this defaults
      to ``"auto"``. Other options are ``True`` (same as ``"optimize"``), ``False``
      (unoptimized), or any string supported by ``opt_einsum``, which
      includes ``"optimize"``,, ``"greedy"``, ``"eager"``, and others.

  Returns:
    A tuple containing the path that may be passed to :func:`~jax.numpy.einsum`, and a
    printable object representing this optimal path.

  Examples:
    >>> key1, key2, key3 = jax.random.split(jax.random.key(0), 3)
    >>> x = jax.random.randint(key1, minval=-5, maxval=5, shape=(2, 3))
    >>> y = jax.random.randint(key2, minval=-5, maxval=5, shape=(3, 100))
    >>> z = jax.random.randint(key3, minval=-5, maxval=5, shape=(100, 5))
    >>> path, path_info = jnp.einsum_path("ij,jk,kl", x, y, z, optimize="optimal")
    >>> print(path)
    [(1, 2), (0, 1)]
    >>> print(path_info)
          Complete contraction:  ij,jk,kl->il
                Naive scaling:  4
            Optimized scaling:  3
              Naive FLOP count:  9.000e+3
          Optimized FLOP count:  3.060e+3
          Theoretical speedup:  2.941e+0
          Largest intermediate:  1.500e+1 elements
        --------------------------------------------------------------------------------
        scaling        BLAS                current                             remaining
        --------------------------------------------------------------------------------
          3           GEMM              kl,jk->lj                             ij,lj->il
          3           GEMM              lj,ij->il                                il->il

    Use the computed path in :func:`~jax.numpy.einsum`:

    >>> jnp.einsum("ij,jk,kl", x, y, z, optimize=path)
    Array([[-754,  324, -142,   82,   50],
           [ 408,  -50,   87,  -29,    7]], dtype=int32)

  .. _opt_einsum: https://github.com/dgasmith/opt_einsum
  """
  if isinstance(optimize, bool):
    optimize2: Any = 'optimal' if optimize else Unoptimized()
  else:
    optimize2 = optimize
  # pyrefly: ignore[no-matching-overload]
  return opt_einsum.contract_path(subscripts, *operands, optimize=optimize2)

