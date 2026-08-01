
def einsum(*args: Any) -> Tensor:
    r"""einsum(equation, *operands) -> Tensor

    Sums the product of the elements of the input :attr:`operands` along dimensions specified using a notation
    based on the Einstein summation convention.

    Einsum allows computing many common multi-dimensional linear algebraic array operations by representing them
    in a short-hand format based on the Einstein summation convention, given by :attr:`equation`. The details of
    this format are described below, but the general idea is to label every dimension of the input :attr:`operands`
    with some subscript and define which subscripts are part of the output. The output is then computed by summing
    the product of the elements of the :attr:`operands` along the dimensions whose subscripts are not part of the
    output. For example, matrix multiplication can be computed using einsum as `torch.einsum("ij,jk->ik", A, B)`.
    Here, j is the summation subscript and i and k the output subscripts (see section below for more details on why).

    Equation:

        The :attr:`equation` string specifies the subscripts (letters in `[a-zA-Z]`) for each dimension of
        the input :attr:`operands` in the same order as the dimensions, separating subscripts for each operand by a
        comma (','), e.g. `'ij,jk'` specify subscripts for two 2D operands. The dimensions labeled with the same subscript
        must be broadcastable, that is, their size must either match or be `1`. The exception is if a subscript is
        repeated for the same input operand, in which case the dimensions labeled with this subscript for this operand
        must match in size and the operand will be replaced by its diagonal along these dimensions. The subscripts that
        appear exactly once in the :attr:`equation` will be part of the output, sorted in increasing alphabetical order.
        The output is computed by multiplying the input :attr:`operands` element-wise, with their dimensions aligned based
        on the subscripts, and then summing out the dimensions whose subscripts are not part of the output.

        Optionally, the output subscripts can be explicitly defined by adding an arrow ('->') at the end of the equation
        followed by the subscripts for the output. For instance, the following equation computes the transpose of a
        matrix multiplication: 'ij,jk->ki'. The output subscripts must appear at least once for some input operand and
        at most once for the output.

        Ellipsis ('...') can be used in place of subscripts to broadcast the dimensions covered by the ellipsis.
        Each input operand may contain at most one ellipsis which will cover the dimensions not covered by subscripts,
        e.g. for an input operand with 5 dimensions, the ellipsis in the equation `'ab...c'` cover the third and fourth
        dimensions. The ellipsis does not need to cover the same number of dimensions across the :attr:`operands` but the
        'shape' of the ellipsis (the size of the dimensions covered by them) must broadcast together. If the output is not
        explicitly defined with the arrow ('->') notation, the ellipsis will come first in the output (left-most dimensions),
        before the subscript labels that appear exactly once for the input operands. e.g. the following equation implements
        batch matrix multiplication `'...ij,...jk'`.

        A few final notes: the equation may contain whitespaces between the different elements (subscripts, ellipsis,
        arrow and comma) but something like `'. . .'` is not valid. An empty string `''` is valid for scalar operands.

    .. note::

        ``torch.einsum`` handles ellipsis ('...') differently from NumPy in that it allows dimensions
        covered by the ellipsis to be summed over, that is, ellipsis are not required to be part of the output.

    .. note::

        Please install opt-einsum (https://optimized-einsum.readthedocs.io/en/stable/) in order to enroll into a more
        performant einsum. You can install when installing torch like so: `pip install torch[opt-einsum]` or by itself
        with `pip install opt-einsum`.

        If opt-einsum is available, this function will automatically speed up computation and/or consume less memory
        by optimizing contraction order through our opt_einsum backend :mod:`torch.backends.opt_einsum` (The _ vs - is
        confusing, I know). This optimization occurs when there are at least three inputs, since the order does not matter
        otherwise. Note that finding `the` optimal path is an NP-hard problem, thus, opt-einsum relies on different
        heuristics to achieve near-optimal results. If opt-einsum is not available, the default order is to contract
        from left to right.

        To bypass this default behavior, add the following to disable opt_einsum and skip path calculation:
        ``torch.backends.opt_einsum.enabled = False``

        To specify which strategy you'd like for opt_einsum to compute the contraction path, add the following line:
        ``torch.backends.opt_einsum.strategy = 'auto'``. The default strategy is 'auto', and we also support 'greedy' and
        'optimal'. Disclaimer that the runtime of 'optimal' is factorial in the number of inputs! See more details in
        the opt_einsum documentation (https://optimized-einsum.readthedocs.io/en/stable/path_finding.html).

    .. note::

        As of PyTorch 1.10 :func:`torch.einsum` also supports the sublist format (see examples below). In this format,
        subscripts for each operand are specified by sublists, list of integers in the range [0, 52). These sublists
        follow their operands, and an extra sublist can appear at the end of the input to specify the output's
        subscripts., e.g. `torch.einsum(op1, sublist1, op2, sublist2, ..., [subslist_out])`. Python's `Ellipsis` object
        may be provided in a sublist to enable broadcasting as described in the Equation section above.

    Args:
        equation (str): The subscripts for the Einstein summation.
        operands (List[Tensor]): The tensors to compute the Einstein summation of.

    Examples::

        >>> # xdoctest: +IGNORE_WANT("non-deterministic")
        >>> # trace
        >>> torch.einsum('ii', torch.randn(4, 4))
        tensor(-1.2104)

        >>> # xdoctest: +IGNORE_WANT("non-deterministic")
        >>> # diagonal
        >>> torch.einsum('ii->i', torch.randn(4, 4))
        tensor([-0.1034,  0.7952, -0.2433,  0.4545])

        >>> # xdoctest: +IGNORE_WANT("non-deterministic")
        >>> # outer product
        >>> x = torch.randn(5)
        >>> y = torch.randn(4)
        >>> torch.einsum('i,j->ij', x, y)
        tensor([[ 0.1156, -0.2897, -0.3918,  0.4963],
                [-0.3744,  0.9381,  1.2685, -1.6070],
                [ 0.7208, -1.8058, -2.4419,  3.0936],
                [ 0.1713, -0.4291, -0.5802,  0.7350],
                [ 0.5704, -1.4290, -1.9323,  2.4480]])

        >>> # xdoctest: +IGNORE_WANT("non-deterministic")
        >>> # batch matrix multiplication
        >>> As = torch.randn(3, 2, 5)
        >>> Bs = torch.randn(3, 5, 4)
        >>> torch.einsum('bij,bjk->bik', As, Bs)
        tensor([[[-1.0564, -1.5904,  3.2023,  3.1271],
                [-1.6706, -0.8097, -0.8025, -2.1183]],

                [[ 4.2239,  0.3107, -0.5756, -0.2354],
                [-1.4558, -0.3460,  1.5087, -0.8530]],

                [[ 2.8153,  1.8787, -4.3839, -1.2112],
                [ 0.3728, -2.1131,  0.0921,  0.8305]]])

        >>> # xdoctest: +IGNORE_WANT("non-deterministic")
        >>> # with sublist format and ellipsis
        >>> torch.einsum(As, [..., 0, 1], Bs, [..., 1, 2], [..., 0, 2])
        tensor([[[-1.0564, -1.5904,  3.2023,  3.1271],
                [-1.6706, -0.8097, -0.8025, -2.1183]],

                [[ 4.2239,  0.3107, -0.5756, -0.2354],
                [-1.4558, -0.3460,  1.5087, -0.8530]],

                [[ 2.8153,  1.8787, -4.3839, -1.2112],
                [ 0.3728, -2.1131,  0.0921,  0.8305]]])

        >>> # batch permute
        >>> A = torch.randn(2, 3, 4, 5)
        >>> torch.einsum('...ij->...ji', A).shape
        torch.Size([2, 3, 5, 4])

        >>> # equivalent to torch.nn.functional.bilinear
        >>> A = torch.randn(3, 5, 4)
        >>> l = torch.randn(2, 5)
        >>> r = torch.randn(2, 4)
        >>> torch.einsum('bn,anm,bm->ba', l, A, r)
        tensor([[-0.3430, -5.2405,  0.4494],
                [ 0.3311,  5.5201, -3.0356]])
    """
    import torch.backends.opt_einsum as opt_einsum

    # This wrapper exists to support variadic args.
    if len(args) < 2:
        raise ValueError(
            "einsum(): must specify the equation string and at least one operand, "
            "or at least one operand and its subscripts list"
        )

    equation = None
    operands = None

    if isinstance(args[0], torch.Tensor):
        # Convert the subscript list format which is an interleaving of operand and its subscripts
        # list with an optional output subscripts list at the end (see documentation for more details on this)
        # to the equation string format by creating the equation string from the subscripts list and grouping the
        # input operands into a tensorlist (List[Tensor]).
        def parse_subscript(n: int) -> str:
            if n == Ellipsis:
                return "..."
            if n >= 0 and n < 26:
                return chr(ord("A") + n)
            if n >= 26 and n < 52:
                return chr(ord("a") + n - 26)
            raise ValueError(
                "einsum(): subscript in subscript list is not within the valid range [0, 52)"
            )

        # Parse subscripts for input operands
        equation = ",".join("".join(parse_subscript(s) for s in l) for l in args[1::2])

        # Parse optional output subscripts (provided when the number of arguments is odd)
        if len(args) % 2 == 1:
            equation += "->" + "".join(parse_subscript(s) for s in args[-1])
            operands = args[:-1:2]
        else:
            operands = args[::2]
    else:
        equation = args[0]
        operands = args[1:]

    if has_torch_function(operands):
        return handle_torch_function(einsum, operands, equation, *operands)

    if len(operands) == 1 and isinstance(operands[0], (list, tuple)):
        # the old interface of passing the operands as one list argument
        _operands = operands[0]
        # recurse in case operands contains value that has torch function
        # in the original implementation this line is omitted
        return einsum(equation, *_operands)

    if len(operands) <= 2 or not opt_einsum.enabled:
        # the path for contracting 0 or 1 time(s) is already optimized
        # or the user has disabled using opt_einsum
        return _VF.einsum(equation, operands)  # type: ignore[attr-defined]

    path = None
    if opt_einsum.is_available():
        _opt_einsum = opt_einsum.get_opt_einsum()
        tupled_path = _opt_einsum.contract_path(
            equation, *operands, optimize=opt_einsum.strategy
        )[0]
        # flatten path for dispatching to C++
        path = [*itertools.chain.from_iterable(tupled_path)]
    return _VF.einsum(equation, operands, path=path)  # type: ignore[attr-defined]


def einsum(*operands, out=None, dtype=None, order="K", casting="safe", optimize=False):
    # Have to manually normalize *operands and **kwargs, following the NumPy signature
    # We have a local import to avoid polluting the global space, as it will be then
    # exported in funcs.py
    from ._ndarray import ndarray
    from ._normalizations import (
        maybe_copy_to,
        normalize_array_like,
        normalize_casting,
        normalize_dtype,
        wrap_tensors,
    )

    dtype = normalize_dtype(dtype)
    casting = normalize_casting(casting)
    if out is not None and not isinstance(out, ndarray):
        raise TypeError("'out' must be an array")
    if order != "K":
        raise NotImplementedError("'order' parameter is not supported.")

    # parse arrays and normalize them
    sublist_format = not isinstance(operands[0], str)
    if sublist_format:
        # op, str, op, str ... [sublistout] format: normalize every other argument

        # - if sublistout is not given, the length of operands is even, and we pick
        #   odd-numbered elements, which are arrays.
        # - if sublistout is given, the length of operands is odd, we peel off
        #   the last one, and pick odd-numbered elements, which are arrays.
        #   Without [:-1], we would have picked sublistout, too.
        array_operands = operands[:-1][::2]
    else:
        # ("ij->", arrays) format
        subscripts, array_operands = operands[0], operands[1:]

    tensors = [normalize_array_like(op) for op in array_operands]
    target_dtype = _dtypes_impl.result_type_impl(*tensors) if dtype is None else dtype

    # work around 'bmm' not implemented for 'Half' etc
    is_half = target_dtype == torch.float16 and all(t.is_cpu for t in tensors)
    if is_half:
        target_dtype = torch.float32

    is_short_int = target_dtype in [torch.uint8, torch.int8, torch.int16, torch.int32]
    if is_short_int:
        target_dtype = torch.int64

    tensors = _util.typecast_tensors(tensors, target_dtype, casting)

    from torch.backends import opt_einsum

    try:
        # set the global state to handle the optimize=... argument, restore on exit
        if opt_einsum.is_available():
            old_strategy = torch.backends.opt_einsum.strategy
            old_enabled = torch.backends.opt_einsum.enabled

            # torch.einsum calls opt_einsum.contract_path, which runs into
            # https://github.com/dgasmith/opt_einsum/issues/219
            # for strategy={True, False}
            if optimize is True:
                optimize = "auto"
            elif optimize is False:
                torch.backends.opt_einsum.enabled = False

            torch.backends.opt_einsum.strategy = optimize

        if sublist_format:
            # recombine operands
            sublists = operands[1::2]
            has_sublistout = len(operands) % 2 == 1
            if has_sublistout:
                sublistout = operands[-1]
            operands = list(itertools.chain.from_iterable(zip(tensors, sublists)))
            if has_sublistout:
                operands.append(sublistout)

            result = torch.einsum(*operands)
        else:
            result = torch.einsum(subscripts, *tensors)

    finally:
        if opt_einsum.is_available():
            torch.backends.opt_einsum.strategy = old_strategy
            torch.backends.opt_einsum.enabled = old_enabled

    result = maybe_copy_to(out, result)
    return wrap_tensors(result)


def einsum(g: jit_utils.GraphContext, equation, tensor_list, path=None):
    tensors = symbolic_helper._unpack_list(tensor_list)
    return _einsum_helper(g, equation, tensors)


def einsum(equation, *operands, **kwargs):
    """Variadic version of torch.einsum to match numpy api."""
    # rename symbols to support PyTorch 0.4.1 and earlier,
    # which allow only symbols a-z.
    equation = convert_to_valid_einsum_chars(equation)

    torch, _ = _get_torch_and_device()
    return torch.einsum(equation, operands)


def einsum(*operands, out=None, optimize=False, **kwargs):
    """
    einsum(subscripts, *operands, out=None, dtype=None, order='K',
           casting='safe', optimize=False)

    Evaluates the Einstein summation convention on the operands.

    Using the Einstein summation convention, many common multi-dimensional,
    linear algebraic array operations can be represented in a simple fashion.
    In *implicit* mode `einsum` computes these values.

    In *explicit* mode, `einsum` provides further flexibility to compute
    other array operations that might not be considered classical Einstein
    summation operations, by disabling, or forcing summation over specified
    subscript labels.

    See the notes and examples for clarification.

    Parameters
    ----------
    subscripts : str
        Specifies the subscripts for summation as comma separated list of
        subscript labels. An implicit (classical Einstein summation)
        calculation is performed unless the explicit indicator '->' is
        included as well as subscript labels of the precise output form.
    operands : list of array_like
        These are the arrays for the operation.
    out : ndarray, optional
        If provided, the calculation is done into this array.
    dtype : {data-type, None}, optional
        If provided, forces the calculation to use the data type specified.
        Note that you may have to also give a more liberal `casting`
        parameter to allow the conversions. Default is None.
    order : {'C', 'F', 'A', 'K'}, optional
        Controls the memory layout of the output. 'C' means it should
        be C contiguous. 'F' means it should be Fortran contiguous,
        'A' means it should be 'F' if the inputs are all 'F', 'C' otherwise.
        'K' means it should be as close to the layout as the inputs as
        is possible, including arbitrarily permuted axes.
        Default is 'K'.
    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        Controls what kind of data casting may occur.  Setting this to
        'unsafe' is not recommended, as it can adversely affect accumulations.

        * 'no' means the data types should not be cast at all.
        * 'equiv' means only byte-order changes are allowed.
        * 'safe' means only casts which can preserve values are allowed.
        * 'same_kind' means only safe casts or casts within a kind,
          like float64 to float32, are allowed.
        * 'unsafe' means any data conversions may be done.

        Default is 'safe'.
    optimize : {False, True, 'greedy', 'optimal'}, optional
        Controls if intermediate optimization should occur. No optimization
        will occur if False and True will default to the 'greedy' algorithm.
        Also accepts an explicit contraction list from the ``np.einsum_path``
        function. See ``np.einsum_path`` for more details. Defaults to False.

    Returns
    -------
    output : ndarray
        The calculation based on the Einstein summation convention.

    See Also
    --------
    einsum_path, dot, inner, outer, tensordot, linalg.multi_dot
    einsum:
        Similar verbose interface is provided by the
        `einops <https://github.com/arogozhnikov/einops>`_ package to cover
        additional operations: transpose, reshape/flatten, repeat/tile,
        squeeze/unsqueeze and reductions.
        The `opt_einsum <https://optimized-einsum.readthedocs.io/en/stable/>`_
        optimizes contraction order for einsum-like expressions
        in backend-agnostic manner.

    Notes
    -----
    The Einstein summation convention can be used to compute
    many multi-dimensional, linear algebraic array operations. `einsum`
    provides a succinct way of representing these.

    A non-exhaustive list of these operations,
    which can be computed by `einsum`, is shown below along with examples:

    * Trace of an array, :py:func:`numpy.trace`.
    * Return a diagonal, :py:func:`numpy.diag`.
    * Array axis summations, :py:func:`numpy.sum`.
    * Transpositions and permutations, :py:func:`numpy.transpose`.
    * Matrix multiplication and dot product, :py:func:`numpy.matmul`
        :py:func:`numpy.dot`.
    * Vector inner and outer products, :py:func:`numpy.inner`
        :py:func:`numpy.outer`.
    * Broadcasting, element-wise and scalar multiplication,
        :py:func:`numpy.multiply`.
    * Tensor contractions, :py:func:`numpy.tensordot`.
    * Chained array operations, in efficient calculation order,
        :py:func:`numpy.einsum_path`.

    The subscripts string is a comma-separated list of subscript labels,
    where each label refers to a dimension of the corresponding operand.
    Whenever a label is repeated it is summed, so ``np.einsum('i,i', a, b)``
    is equivalent to :py:func:`np.inner(a,b) <numpy.inner>`. If a label
    appears only once, it is not summed, so ``np.einsum('i', a)``
    produces a view of ``a`` with no changes. A further example
    ``np.einsum('ij,jk', a, b)`` describes traditional matrix multiplication
    and is equivalent to :py:func:`np.matmul(a,b) <numpy.matmul>`.
    Repeated subscript labels in one operand take the diagonal.
    For example, ``np.einsum('ii', a)`` is equivalent to
    :py:func:`np.trace(a) <numpy.trace>`.

    In *implicit mode*, the chosen subscripts are important
    since the axes of the output are reordered alphabetically.  This
    means that ``np.einsum('ij', a)`` doesn't affect a 2D array, while
    ``np.einsum('ji', a)`` takes its transpose. Additionally,
    ``np.einsum('ij,jk', a, b)`` returns a matrix multiplication, while,
    ``np.einsum('ij,jh', a, b)`` returns the transpose of the
    multiplication since subscript 'h' precedes subscript 'i'.

    In *explicit mode* the output can be directly controlled by
    specifying output subscript labels.  This requires the
    identifier '->' as well as the list of output subscript labels.
    This feature increases the flexibility of the function since
    summing can be disabled or forced when required. The call
    ``np.einsum('i->', a)`` is like :py:func:`np.sum(a) <numpy.sum>`
    if ``a`` is a 1-D array, and ``np.einsum('ii->i', a)``
    is like :py:func:`np.diag(a) <numpy.diag>` if ``a`` is a square 2-D array.
    The difference is that `einsum` does not allow broadcasting by default.
    Additionally ``np.einsum('ij,jh->ih', a, b)`` directly specifies the
    order of the output subscript labels and therefore returns matrix
    multiplication, unlike the example above in implicit mode.

    To enable and control broadcasting, use an ellipsis.  Default
    NumPy-style broadcasting is done by adding an ellipsis
    to the left of each term, like ``np.einsum('...ii->...i', a)``.
    ``np.einsum('...i->...', a)`` is like
    :py:func:`np.sum(a, axis=-1) <numpy.sum>` for array ``a`` of any shape.
    To take the trace along the first and last axes,
    you can do ``np.einsum('i...i', a)``, or to do a matrix-matrix
    product with the left-most indices instead of rightmost, one can do
    ``np.einsum('ij...,jk...->ik...', a, b)``.

    When there is only one operand, no axes are summed, and no output
    parameter is provided, a view into the operand is returned instead
    of a new array.  Thus, taking the diagonal as ``np.einsum('ii->i', a)``
    produces a view (changed in version 1.10.0).

    `einsum` also provides an alternative way to provide the subscripts and
    operands as ``einsum(op0, sublist0, op1, sublist1, ..., [sublistout])``.
    If the output shape is not provided in this format `einsum` will be
    calculated in implicit mode, otherwise it will be performed explicitly.
    The examples below have corresponding `einsum` calls with the two
    parameter methods.

    Views returned from einsum are now writeable whenever the input array
    is writeable. For example, ``np.einsum('ijk...->kji...', a)`` will now
    have the same effect as :py:func:`np.swapaxes(a, 0, 2) <numpy.swapaxes>`
    and ``np.einsum('ii->i', a)`` will return a writeable view of the diagonal
    of a 2D array.

    Added the ``optimize`` argument which will optimize the contraction order
    of an einsum expression. For a contraction with three or more operands
    this can greatly increase the computational efficiency at the cost of
    a larger memory footprint during computation.

    Typically a 'greedy' algorithm is applied which empirical tests have shown
    returns the optimal path in the majority of cases. In some cases 'optimal'
    will return the superlative path through a more expensive, exhaustive
    search. For iterative calculations it may be advisable to calculate
    the optimal path once and reuse that path by supplying it as an argument.
    An example is given below.

    See :py:func:`numpy.einsum_path` for more details.

    Examples
    --------
    >>> a = np.arange(25).reshape(5,5)
    >>> b = np.arange(5)
    >>> c = np.arange(6).reshape(2,3)

    Trace of a matrix:

    >>> np.einsum('ii', a)
    60
    >>> np.einsum(a, [0,0])
    60
    >>> np.trace(a)
    60

    Extract the diagonal (requires explicit form):

    >>> np.einsum('ii->i', a)
    array([ 0,  6, 12, 18, 24])
    >>> np.einsum(a, [0,0], [0])
    array([ 0,  6, 12, 18, 24])
    >>> np.diag(a)
    array([ 0,  6, 12, 18, 24])

    Sum over an axis (requires explicit form):

    >>> np.einsum('ij->i', a)
    array([ 10,  35,  60,  85, 110])
    >>> np.einsum(a, [0,1], [0])
    array([ 10,  35,  60,  85, 110])
    >>> np.sum(a, axis=1)
    array([ 10,  35,  60,  85, 110])

    For higher dimensional arrays summing a single axis can be done
    with ellipsis:

    >>> np.einsum('...j->...', a)
    array([ 10,  35,  60,  85, 110])
    >>> np.einsum(a, [Ellipsis,1], [Ellipsis])
    array([ 10,  35,  60,  85, 110])

    Compute a matrix transpose, or reorder any number of axes:

    >>> np.einsum('ji', c)
    array([[0, 3],
           [1, 4],
           [2, 5]])
    >>> np.einsum('ij->ji', c)
    array([[0, 3],
           [1, 4],
           [2, 5]])
    >>> np.einsum(c, [1,0])
    array([[0, 3],
           [1, 4],
           [2, 5]])
    >>> np.transpose(c)
    array([[0, 3],
           [1, 4],
           [2, 5]])

    Vector inner products:

    >>> np.einsum('i,i', b, b)
    30
    >>> np.einsum(b, [0], b, [0])
    30
    >>> np.inner(b,b)
    30

    Matrix vector multiplication:

    >>> np.einsum('ij,j', a, b)
    array([ 30,  80, 130, 180, 230])
    >>> np.einsum(a, [0,1], b, [1])
    array([ 30,  80, 130, 180, 230])
    >>> np.dot(a, b)
    array([ 30,  80, 130, 180, 230])
    >>> np.einsum('...j,j', a, b)
    array([ 30,  80, 130, 180, 230])

    Broadcasting and scalar multiplication:

    >>> np.einsum('..., ...', 3, c)
    array([[ 0,  3,  6],
           [ 9, 12, 15]])
    >>> np.einsum(',ij', 3, c)
    array([[ 0,  3,  6],
           [ 9, 12, 15]])
    >>> np.einsum(3, [Ellipsis], c, [Ellipsis])
    array([[ 0,  3,  6],
           [ 9, 12, 15]])
    >>> np.multiply(3, c)
    array([[ 0,  3,  6],
           [ 9, 12, 15]])

    Vector outer product:

    >>> np.einsum('i,j', np.arange(2)+1, b)
    array([[0, 1, 2, 3, 4],
           [0, 2, 4, 6, 8]])
    >>> np.einsum(np.arange(2)+1, [0], b, [1])
    array([[0, 1, 2, 3, 4],
           [0, 2, 4, 6, 8]])
    >>> np.outer(np.arange(2)+1, b)
    array([[0, 1, 2, 3, 4],
           [0, 2, 4, 6, 8]])

    Tensor contraction:

    >>> a = np.arange(60.).reshape(3,4,5)
    >>> b = np.arange(24.).reshape(4,3,2)
    >>> np.einsum('ijk,jil->kl', a, b)
    array([[4400., 4730.],
           [4532., 4874.],
           [4664., 5018.],
           [4796., 5162.],
           [4928., 5306.]])
    >>> np.einsum(a, [0,1,2], b, [1,0,3], [2,3])
    array([[4400., 4730.],
           [4532., 4874.],
           [4664., 5018.],
           [4796., 5162.],
           [4928., 5306.]])
    >>> np.tensordot(a,b, axes=([1,0],[0,1]))
    array([[4400., 4730.],
           [4532., 4874.],
           [4664., 5018.],
           [4796., 5162.],
           [4928., 5306.]])

    Writeable returned arrays (since version 1.10.0):

    >>> a = np.zeros((3, 3))
    >>> np.einsum('ii->i', a)[:] = 1
    >>> a
    array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]])

    Example of ellipsis use:

    >>> a = np.arange(6).reshape((3,2))
    >>> b = np.arange(12).reshape((4,3))
    >>> np.einsum('ki,jk->ij', a, b)
    array([[10, 28, 46, 64],
           [13, 40, 67, 94]])
    >>> np.einsum('ki,...k->i...', a, b)
    array([[10, 28, 46, 64],
           [13, 40, 67, 94]])
    >>> np.einsum('k...,jk', a, b)
    array([[10, 28, 46, 64],
           [13, 40, 67, 94]])

    Chained array operations. For more complicated contractions, speed ups
    might be achieved by repeatedly computing a 'greedy' path or pre-computing
    the 'optimal' path and repeatedly applying it, using an `einsum_path`
    insertion (since version 1.12.0). Performance improvements can be
    particularly significant with larger arrays:

    >>> a = np.ones(64).reshape(2,4,8)

    Basic `einsum`: ~1520ms  (benchmarked on 3.1GHz Intel i5.)

    >>> for iteration in range(500):
    ...     _ = np.einsum('ijk,ilm,njm,nlk,abc->',a,a,a,a,a)

    Sub-optimal `einsum` (due to repeated path calculation time): ~330ms

    >>> for iteration in range(500):
    ...     _ = np.einsum('ijk,ilm,njm,nlk,abc->',a,a,a,a,a,
    ...         optimize='optimal')

    Greedy `einsum` (faster optimal path approximation): ~160ms

    >>> for iteration in range(500):
    ...     _ = np.einsum('ijk,ilm,njm,nlk,abc->',a,a,a,a,a, optimize='greedy')

    Optimal `einsum` (best usage pattern in some use cases): ~110ms

    >>> path = np.einsum_path('ijk,ilm,njm,nlk,abc->',a,a,a,a,a,
    ...     optimize='optimal')[0]
    >>> for iteration in range(500):
    ...     _ = np.einsum('ijk,ilm,njm,nlk,abc->',a,a,a,a,a, optimize=path)

    """
    # Special handling if out is specified
    specified_out = out is not None

    # If no optimization, run pure einsum
    if optimize is False:
        if specified_out:
            kwargs['out'] = out
        return c_einsum(*operands, **kwargs)

    # Check the kwargs to avoid a more cryptic error later, without having to
    # repeat default values here
    valid_einsum_kwargs = ['dtype', 'order', 'casting']
    unknown_kwargs = [k for k in kwargs if k not in valid_einsum_kwargs]
    if len(unknown_kwargs):
        raise TypeError(f"Did not understand the following kwargs: {unknown_kwargs}")

    # Build the contraction list and operand
    operands, contraction_list = einsum_path(*operands, optimize=optimize,
                                             einsum_call=True)

    # Start contraction loop
    for num, contraction in enumerate(contraction_list):
        inds, einsum_str, _ = contraction
        tmp_operands = [operands.pop(x) for x in inds]

        # Do we need to deal with the output?
        handle_out = specified_out and ((num + 1) == len(contraction_list))

        # If out was specified
        if handle_out:
            kwargs["out"] = out

        if len(tmp_operands) == 2:
            # Call (batched) matrix multiplication if possible
            new_view = bmm_einsum(einsum_str, *tmp_operands, **kwargs)
        else:
            # Call einsum
            new_view = c_einsum(einsum_str, *tmp_operands, **kwargs)

        # Append new items and dereference what we can
        operands.append(new_view)
        del tmp_operands, new_view

    if specified_out:
        return out
    else:
        return operands[0]


def einsum(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], einsum_config: _Union[str, _ods_ir.StringAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return EinsumOp(result=result, lhs=lhs, rhs=rhs, einsum_config=einsum_config, loc=loc, ip=ip).result


def einsum(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], einsum_config: _Union[str, _ods_ir.StringAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return EinsumOp(result=result, lhs=lhs, rhs=rhs, einsum_config=einsum_config, loc=loc, ip=ip).result


def einsum(
    subscript: str, /,
    *operands: ArrayLike,
    out: None = None,
    optimize: str | bool | list[tuple[int, ...]] = "auto",
    precision: lax.PrecisionLike = None,
    preferred_element_type: DTypeLike | None = None,
    _dot_general: Callable[..., Array] = lax.dot_general,
    out_sharding=None,
) -> Array: ...


def einsum(
    arr: ArrayLike,
    axes: Sequence[Any], /,
    *operands: ArrayLike | Sequence[Any],
    out: None = None,
    optimize: str | bool | list[tuple[int, ...]] = "auto",
    precision: lax.PrecisionLike = None,
    preferred_element_type: DTypeLike | None = None,
    _dot_general: Callable[..., Array] = lax.dot_general,
    out_sharding=None,
) -> Array: ...


def einsum(
    subscripts, /,
    *operands,
    out: None = None,
    optimize: str | bool | list[tuple[int, ...]] = "auto",
    precision: lax.PrecisionLike = None,
    preferred_element_type: DTypeLike | None = None,
    _dot_general: Callable[..., Array] = lax.dot_general,
    out_sharding=None,
) -> Array:
  """Einstein summation

  JAX implementation of :func:`numpy.einsum`.

  ``einsum`` is a powerful and generic API for computing various reductions,
  inner products, outer products, axis reorderings, and combinations thereof
  across one or more input arrays. It has a somewhat complicated overloaded API;
  the arguments below reflect the most common calling convention. The Examples
  section below demonstrates some of the alternative calling conventions.

  Args:
    subscripts: string containing axes names separated by commas.
    *operands: sequence of one or more arrays corresponding to the subscripts.
    optimize: specify how to optimize the order of computation. In JAX this defaults
      to ``"auto"`` which produces optimized expressions via the opt_einsum_
      package. Other options are ``True`` (same as ``"optimal"``), ``False``
      (unoptimized), or any string supported by ``opt_einsum``, which
      includes ``"optimal"``, ``"greedy"``, ``"eager"``, and others. It may also
      be a pre-computed path (see :func:`~jax.numpy.einsum_path`).
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``).
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.
    out: unsupported by JAX
    _dot_general: optionally override the ``dot_general`` callable used by ``einsum``.
      This parameter is experimental, and may be removed without warning at any time.

  Returns:
    array containing the result of the einstein summation.

  See also:
    :func:`jax.numpy.einsum_path`

  Examples:
    The mechanics of ``einsum`` are perhaps best demonstrated by example. Here we
    show how to use ``einsum`` to compute a number of quantities from one or more
    arrays. For more discussion and examples of ``einsum``, see the documentation
    of :func:`numpy.einsum`.

    >>> M = jnp.arange(16).reshape(4, 4)
    >>> x = jnp.arange(4)
    >>> y = jnp.array([5, 4, 3, 2])

    **Vector product**

    >>> jnp.einsum('i,i', x, y)
    Array(16, dtype=int32)
    >>> jnp.vecdot(x, y)
    Array(16, dtype=int32)

    Here are some alternative ``einsum`` calling conventions to compute the same
    result:

    >>> jnp.einsum('i,i->', x, y)  # explicit form
    Array(16, dtype=int32)
    >>> jnp.einsum(x, (0,), y, (0,))  # implicit form via indices
    Array(16, dtype=int32)
    >>> jnp.einsum(x, (0,), y, (0,), ())  # explicit form via indices
    Array(16, dtype=int32)

    **Matrix product**

    >>> jnp.einsum('ij,j->i', M, x)  # explicit form
    Array([14, 38, 62, 86], dtype=int32)
    >>> jnp.matmul(M, x)
    Array([14, 38, 62, 86], dtype=int32)

    Here are some alternative ``einsum`` calling conventions to compute the same
    result:

    >>> jnp.einsum('ij,j', M, x) # implicit form
    Array([14, 38, 62, 86], dtype=int32)
    >>> jnp.einsum(M, (0, 1), x, (1,), (0,)) # explicit form via indices
    Array([14, 38, 62, 86], dtype=int32)
    >>> jnp.einsum(M, (0, 1), x, (1,))  # implicit form via indices
    Array([14, 38, 62, 86], dtype=int32)

    **Outer product**

    >>> jnp.einsum("i,j->ij", x, y)
    Array([[ 0,  0,  0,  0],
           [ 5,  4,  3,  2],
           [10,  8,  6,  4],
           [15, 12,  9,  6]], dtype=int32)
    >>> jnp.outer(x, y)
    Array([[ 0,  0,  0,  0],
           [ 5,  4,  3,  2],
           [10,  8,  6,  4],
           [15, 12,  9,  6]], dtype=int32)

    Some other ways of computing outer products:

    >>> jnp.einsum("i,j", x, y)  # implicit form
    Array([[ 0,  0,  0,  0],
           [ 5,  4,  3,  2],
           [10,  8,  6,  4],
           [15, 12,  9,  6]], dtype=int32)
    >>> jnp.einsum(x, (0,), y, (1,), (0, 1))  # explicit form via indices
    Array([[ 0,  0,  0,  0],
           [ 5,  4,  3,  2],
           [10,  8,  6,  4],
           [15, 12,  9,  6]], dtype=int32)
    >>> jnp.einsum(x, (0,), y, (1,))  # implicit form via indices
    Array([[ 0,  0,  0,  0],
           [ 5,  4,  3,  2],
           [10,  8,  6,  4],
           [15, 12,  9,  6]], dtype=int32)

    **1D array sum**

    >>> jnp.einsum("i->", x)  # requires explicit form
    Array(6, dtype=int32)
    >>> jnp.einsum(x, (0,), ())  # explicit form via indices
    Array(6, dtype=int32)
    >>> jnp.sum(x)
    Array(6, dtype=int32)

    **Sum along an axis**

    >>> jnp.einsum("...j->...", M)  # requires explicit form
    Array([ 6, 22, 38, 54], dtype=int32)
    >>> jnp.einsum(M, (..., 0), (...,))  # explicit form via indices
    Array([ 6, 22, 38, 54], dtype=int32)
    >>> M.sum(-1)
    Array([ 6, 22, 38, 54], dtype=int32)

    **Matrix transpose**

    >>> y = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.einsum("ij->ji", y)  # explicit form
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)
    >>> jnp.einsum("ji", y)  # implicit form
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)
    >>> jnp.einsum(y, (1, 0))  # implicit form via indices
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)
    >>> jnp.einsum(y, (0, 1), (1, 0))  # explicit form via indices
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)
    >>> jnp.transpose(y)
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)

    **Matrix diagonal**

    >>> jnp.einsum("ii->i", M)
    Array([ 0,  5, 10, 15], dtype=int32)
    >>> jnp.diagonal(M)
    Array([ 0,  5, 10, 15], dtype=int32)

    **Matrix trace**

    >>> jnp.einsum("ii", M)
    Array(30, dtype=int32)
    >>> jnp.trace(M)
    Array(30, dtype=int32)

    **Tensor products**

    >>> x = jnp.arange(30).reshape(2, 3, 5)
    >>> y = jnp.arange(60).reshape(3, 4, 5)
    >>> jnp.einsum('ijk,jlk->il', x, y)  # explicit form
    Array([[ 3340,  3865,  4390,  4915],
           [ 8290,  9940, 11590, 13240]], dtype=int32)
    >>> jnp.tensordot(x, y, axes=[(1, 2), (0, 2)])
    Array([[ 3340,  3865,  4390,  4915],
           [ 8290,  9940, 11590, 13240]], dtype=int32)
    >>> jnp.einsum('ijk,jlk', x, y)  # implicit form
    Array([[ 3340,  3865,  4390,  4915],
           [ 8290,  9940, 11590, 13240]], dtype=int32)
    >>> jnp.einsum(x, (0, 1, 2), y, (1, 3, 2), (0, 3))  # explicit form via indices
    Array([[ 3340,  3865,  4390,  4915],
           [ 8290,  9940, 11590, 13240]], dtype=int32)
    >>> jnp.einsum(x, (0, 1, 2), y, (1, 3, 2))  # implicit form via indices
    Array([[ 3340,  3865,  4390,  4915],
           [ 8290,  9940, 11590, 13240]], dtype=int32)

    **Chained dot products**

    >>> w = jnp.arange(5, 9).reshape(2, 2)
    >>> x = jnp.arange(6).reshape(2, 3)
    >>> y = jnp.arange(-2, 4).reshape(3, 2)
    >>> z = jnp.array([[2, 4, 6], [3, 5, 7]])
    >>> jnp.einsum('ij,jk,kl,lm->im', w, x, y, z)
    Array([[ 481,  831, 1181],
           [ 651, 1125, 1599]], dtype=int32)
    >>> jnp.einsum(w, (0, 1), x, (1, 2), y, (2, 3), z, (3, 4))  # implicit, via indices
    Array([[ 481,  831, 1181],
           [ 651, 1125, 1599]], dtype=int32)
    >>> w @ x @ y @ z  # direct chain of matmuls
    Array([[ 481,  831, 1181],
           [ 651, 1125, 1599]], dtype=int32)
    >>> jnp.linalg.multi_dot([w, x, y, z])
    Array([[ 481,  831, 1181],
           [ 651, 1125, 1599]], dtype=int32)

  .. _opt_einsum: https://github.com/dgasmith/opt_einsum
  """
  operands = (subscripts, *operands)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.einsum is not supported.")
  spec = operands[0] if isinstance(operands[0], str) else None
  path_type = 'optimal' if optimize is True else Unoptimized() if optimize is False else optimize

  # Extract __jax_array__ before passing to contract_path()
  def _convert(op):
    m = getattr(op, "__jax_array__", None)
    return m() if m is not None else op
  operands = tuple(_convert(op) for op in operands)

  # Allow handling of shape polymorphism
  non_constant_dim_types = {
      type(d) for op in operands if not isinstance(op, str)
      for d in np.shape(op) if not core.is_constant_dim(d)
  }
  if not non_constant_dim_types:
    contract_path: Any = opt_einsum.contract_path
  else:
    ty = next(iter(non_constant_dim_types))
    contract_path = _poly_einsum_handlers.get(ty, _default_poly_einsum_handler)
  # using einsum_call=True here is an internal api for opt_einsum... sorry
  operands, contractions = contract_path(
        *operands, einsum_call=True, use_blas=True, optimize=path_type)

  contractions = tuple((a, frozenset(b), c) for a, b, c, *_ in contractions)
  num_contractions = len(contractions)

  out_sharding = canonicalize_sharding(out_sharding, 'einsum')
  if out_sharding is not None and not isinstance(out_sharding, NamedSharding):
    raise NotImplementedError(
        "`out_sharding` argument of `einsum` only supports NamedSharding"
        " instances.")

  jit_einsum = api.jit(_einsum, static_argnums=(1, 2, 3, 4, 5), inline=True)
  if spec is not None:
    jit_einsum = api.named_call(jit_einsum, name=spec)
  operand_arrays = list(util.ensure_arraylike_tuple("einsum", operands))

  if num_contractions > 1 and out_sharding is not None:
    # TODO(yashkatariya): If the out_sharding is unreduced, figure out a way to
    # run the dot_general unreduced_rule on these einsums because right now we
    # drop into Auto mode skipping the checks happening in the rule.
    return auto_axes(
        jit_einsum,
        axes=out_sharding.mesh.explicit_axes,
        out_sharding=out_sharding,
    )(operand_arrays, contractions=contractions, precision=precision,
      preferred_element_type=preferred_element_type, _dot_general=_dot_general,
      out_sharding=None)
  else:
    return jit_einsum(operand_arrays, contractions, precision,
                      preferred_element_type, _dot_general, out_sharding)

