
def composite(image1: Image, image2: Image, mask: Image) -> Image:
    """
    Create composite image by blending images using a transparency mask.

    :param image1: The first image.
    :param image2: The second image.  Must have the same mode and
       size as the first image.
    :param mask: A mask image.  This image can have mode
       "1", "L", or "RGBA", and must have the same size as the
       other two images.
    """

    image = image2.copy()
    image.paste(image1, None, mask)
    return image


def composite(
    image1: Image.Image, image2: Image.Image, mask: Image.Image
) -> Image.Image:
    """Create composite using transparency mask. Alias for
    :py:func:`PIL.Image.composite`.

    :rtype: :py:class:`~PIL.Image.Image`
    """

    return Image.composite(image1, image2, mask)


def composite(nth):
    """ Return the nth composite number, with the composite numbers indexed as
        composite(1) = 4, composite(2) = 6, etc....

        Examples
        ========

        >>> from sympy import composite
        >>> composite(36)
        52
        >>> composite(1)
        4
        >>> composite(17737)
        20000

        See Also
        ========

        sympy.ntheory.primetest.isprime : Test if n is prime
        primerange : Generate all primes in a given range
        primepi : Return the number of primes less than or equal to n
        prime : Return the nth prime
        compositepi : Return the number of positive composite numbers less than or equal to n
    """
    n = as_int(nth)
    if n < 1:
        raise ValueError("nth must be a positive integer; composite(1) == 4")
    composite_arr = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18]
    if n <= 10:
        return composite_arr[n - 1]

    a, b = 4, sieve._list[-1]
    if n <= b - _primepi(b) - 1:
        while a < b - 1:
            mid = (a + b) >> 1
            if mid - _primepi(mid) - 1 > n:
                b = mid
            else:
                a = mid
        if isprime(a):
            a -= 1
        return a

    from sympy.functions.elementary.exponential import log
    from sympy.functions.special.error_functions import li
    a = 4 # Lower bound for binary search
    b = int(n*(log(n) + log(log(n)))) # Upper bound for the search.

    while a < b:
        mid = (a + b) >> 1
        if mid - li(mid) - 1 > n:
            b = mid
        else:
            a = mid + 1

    n_composites = a - _primepi(a) - 1
    while n_composites > n:
        if not isprime(a):
            n_composites -= 1
        a -= 1
    if isprime(a):
        a -= 1
    return a


def composite(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value], name: _Union[str, _ods_ir.StringAttr], decomposition: _Union[str, _ods_ir.FlatSymbolRefAttr], num_composite_regions: int, *, composite_attributes: _Optional[_Union[dict, _ods_ir.DictAttr]] = None, version: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CompositeOp]:
  op = CompositeOp(result=result, inputs=inputs, name=name, decomposition=decomposition, num_composite_regions=num_composite_regions, composite_attributes=composite_attributes, version=version, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def composite(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value], name: _Union[str, _ods_ir.StringAttr], decomposition: _Union[str, _ods_ir.FlatSymbolRefAttr], num_composite_regions: int, *, composite_attributes: _Optional[_Union[dict, _ods_ir.DictAttr]] = None, version: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CompositeOp]:
  op = CompositeOp(result=result, inputs=inputs, name=name, decomposition=decomposition, num_composite_regions=num_composite_regions, composite_attributes=composite_attributes, version=version, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def composite(
    decomposition: Callable,
    name: str,
    version: int = 0,
):
  """Composite with semantics defined by the decomposition function.

  A composite is a higher-order JAX function that encapsulates an operation made
  up (composed) of other JAX functions. The semantics of the op are implemented
  by the ``decomposition`` function. In other words, the defined composite
  function can be replaced with its decomposed implementation without changing
  the semantics of the encapsulated operation.

  The compiler can recognize specific composite operations by their ``name``,
  ``version``, ``kwargs``, and dtypes to emit more efficient code, potentially
  leveraging hardware-specific instructions or optimizations. If the compiler
  doesn't recognize the composite, it falls back to compiling the
  ``decomposition`` function.

  Consider a "tangent" composite operation. Its ``decomposition`` function could
  be implemented as ``sin(x) / cos(x)``. A hardware-aware compiler could
  recognize the "tangent" composite and emit a single ``tangent`` instruction
  instead of three separate instructions (``sin``, ``divide``, and ``cos``).
  For hardware without dedicated tangent support, it would fall back to
  compiling the decomposition.

  This is useful for preserving high-level abstractions that would otherwise be
  lost while lowering, which allows for easier pattern-matching in low-level IR.

  Args:
    decomposition: function that implements the semantics of the composite op.
    name: name of the encapsulated operation.
    version: optional int to indicate semantic changes to the composite.

  Returns:
    Callable: Returns a composite function. Note that positional arguments to
    this function should be interpreted as inputs and keyword arguments should
    be interpreted as attributes of the op. Any keyword arguments that are
    passed with ``None`` as a value will be omitted from the
    ``composite_attributes``.

  Examples:
    Tangent kernel:

    >>> def my_tangent_composite(x):
    ...   return lax.composite(
    ...     lambda x: lax.sin(x) / lax.cos(x), name="my.tangent"
    ...   )(x)
    >>>
    >>> pi = jnp.pi
    >>> x = jnp.array([0.0, pi / 4, 3 * pi / 4, pi])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   print(my_tangent_composite(x))
    ...   print(lax.tan(x))
    [ 0.  1. -1.  0.]
    [ 0.  1. -1.  0.]

    The recommended way to create composites is via a decorator. Use ``/`` and
    ``*`` in the function signature to be explicit about positional and keyword
    arguments, respectively:

    >>> @partial(lax.composite, name="my.softmax")
    ... def my_softmax_composite(x, /, *, axis):
    ...   return jax.nn.softmax(x, axis)
  """
  @functools.wraps(decomposition)
  def _decorator(*args, **kwargs):
    debug_info = api_util.debug_info("composite", decomposition,
                                     args, {})
    flat_args, in_tree = tree_util.tree_flatten(args)
    in_avals = tuple(core.typeof(x) for x in flat_args)
    if any(isinstance(v, core.Tracer) for v in kwargs.values()):
      raise UnexpectedTracerError(
          "Found a JAX Tracer as an attribute in the decomposition for the "
          f"composite op '{name}'. This means that the decomposition function "
          "closes over a value that is involved in a JAX transformation. "
          "Any values that aren't explicitly known at compile time must be "
          "explicitly passed as arguments to the composite."
          "\n\nNote: If you are passing jax arrays as attributes, use numpy "
          "arrays instead.")
    closed_jaxpr, consts, out_tree = _trace_composite_to_jaxpr(
        partial(decomposition, **kwargs), in_tree, in_avals, name, debug_info
    )
    attributes = []
    for k, v in kwargs.items():
      leaves, treedef = tree_util.tree_flatten(v)
      leaves = tuple(
          HashableArray(v) if isinstance(v, np.ndarray) else v for v in leaves
      )
      attributes.append((k, leaves, treedef))
    flat_consts_and_args = core.auto_insert_reshard(*consts, *flat_args)
    out_flat = composite_p.bind(
        *flat_consts_and_args,
        name=name,
        attributes=tuple(attributes),
        version=version,
        jaxpr=closed_jaxpr,
    )
    return tree_util.tree_unflatten(out_tree, out_flat)

  return _decorator

