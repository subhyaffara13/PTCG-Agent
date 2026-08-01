
def fold(
    input: Tensor,
    output_size: BroadcastingList2[int],
    kernel_size: BroadcastingList2[int],
    dilation: BroadcastingList2[int] = 1,
    padding: BroadcastingList2[int] = 0,
    stride: BroadcastingList2[int] = 1,
) -> Tensor:
    r"""Combine an array of sliding local blocks into a large containing tensor.

    .. warning::
        Currently, only unbatched (3D) or batched (4D) image-like output tensors are supported.

    See :class:`torch.nn.Fold` for details
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            fold,
            (input,),
            input,
            output_size,
            kernel_size,
            dilation=dilation,
            padding=padding,
            stride=stride,
        )
    return torch._C._nn.col2im(
        input,
        _pair(output_size),
        _pair(kernel_size),
        _pair(dilation),
        _pair(padding),
        _pair(stride),
    )


def fold(binop, seq, default=no_default, map=map, chunksize=128, combine=None):
    """
    Reduce without guarantee of ordered reduction.

    Parameters
    ----------
    binops
        Associative operator. The associative property allows us to
        leverage a parallel map to perform reductions in parallel.


    inputs:

    ``binop``     - associative operator. The associative property allows us to
                    leverage a parallel map to perform reductions in parallel.

    ``seq``       - a sequence to be aggregated
    ``default``   - an identity element like 0 for ``add`` or 1 for mul

    ``map``       - an implementation of ``map``. This may be parallel and
                    determines how work is distributed.
    ``chunksize`` - Number of elements of ``seq`` that should be handled
                    within a single function call
    ``combine``   - Binary operator to combine two intermediate results.
                    If ``binop`` is of type (total, item) -> total
                    then ``combine`` is of type (total, total) -> total
                    Defaults to ``binop`` for common case of operators like add

    Fold chunks up the collection into blocks of size ``chunksize`` and then
    feeds each of these to calls to ``reduce``. This work is distributed
    with a call to ``map``, gathered back and then refolded to finish the
    computation. In this way ``fold`` specifies only how to chunk up data but
    leaves the distribution of this work to an externally provided ``map``
    function. This function can be sequential or rely on multithreading,
    multiprocessing, or even distributed solutions.

    If ``map`` intends to serialize functions it should be prepared to accept
    and serialize lambdas. Note that the standard ``pickle`` module fails
    here.

    Example
    -------

    >>> # Provide a parallel map to accomplish a parallel sum
    >>> from operator import add
    >>> fold(add, [1, 2, 3, 4], chunksize=2, map=map)
    10
    """
    assert chunksize > 1

    if combine is None:
        combine = binop

    chunks = partition_all(chunksize, seq)

    # Evaluate sequence in chunks via map
    if default == no_default:
        results = map(
            functools.partial(_reduce, binop),
            chunks)
    else:
        results = map(
            functools.partial(_reduce, binop, initial=default),
            chunks)

    results = list(results)  # TODO: Support complete laziness

    if len(results) == 1:    # Return completed result
        return results[0]
    else:                    # Recurse to reaggregate intermediate results
        return fold(combine, results, map=map, chunksize=chunksize)

