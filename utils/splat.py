import functools

def splat(func):
    """
    Wrap func to expect its parameters to be passed positionally in a tuple.

    Has a similar effect to that of ``itertools.starmap`` over
    simple ``map``.

    >>> pairs = [(-1, 1), (0, 2)]
    >>> more_itertools.consume(itertools.starmap(print, pairs))
    -1 1
    0 2
    >>> more_itertools.consume(map(splat(print), pairs))
    -1 1
    0 2

    The approach generalizes to other iterators that don't have a "star"
    equivalent, such as a "starfilter".

    >>> list(filter(splat(operator.add), pairs))
    [(0, 2)]

    Splat also accepts a mapping argument.

    >>> def is_nice(msg, code):
    ...     return "smile" in msg or code == 0
    >>> msgs = [
    ...     dict(msg='smile!', code=20),
    ...     dict(msg='error :(', code=1),
    ...     dict(msg='unknown', code=0),
    ... ]
    >>> for msg in filter(splat(is_nice), msgs):
    ...     print(msg)
    {'msg': 'smile!', 'code': 20}
    {'msg': 'unknown', 'code': 0}
    """
    return functools.wraps(func)(functools.partial(_splat_inner, func=func))


def splat(result: _ods_ir.Type, src: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SplatOp(result=result, src=src, loc=loc, ip=ip).result

