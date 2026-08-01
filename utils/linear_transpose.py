
def linear_transpose(
    input: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor | None
) -> torch.Tensor:
    if bias is None:
        return torch.matmul(weight, input.transpose(-1, -2))
    return torch.matmul(weight, input.transpose(-1, -2)) + bias.unsqueeze(-1)


def linear_transpose(fun: Callable, *primals, reduce_axes=()) -> Callable:
  """Transpose a function that is promised to be linear.

  For linear functions, this transformation is equivalent to :py:func:`vjp`, but
  avoids the overhead of computing the forward pass.

  The outputs of the transposed function will always have the exact same dtypes
  as ``primals``, even if some values are truncated (e.g., from complex to
  float, or from float64 to float32). To avoid truncation, use dtypes in
  ``primals`` that match the full range of desired outputs from the transposed
  function. Integer dtypes are not supported.

  Args:
    fun: the linear function to be transposed.
    *primals: a positional argument tuple of arrays, scalars, or (nested)
      standard Python containers (tuples, lists, dicts, namedtuples, i.e.,
      pytrees) of those types used for evaluating the shape/dtype of
      ``fun(*primals)``. These arguments may be real scalars/ndarrays, but that
      is not required: only the ``shape`` and ``dtype`` attributes are accessed.
      See below for an example. (Note that the duck-typed objects cannot be
      namedtuples because those are treated as standard Python containers.)

  Returns:
    A callable that calculates the transpose of ``fun``. Valid input into this
    function must have the same shape/dtypes/structure as the result of
    ``fun(*primals)``. Output will be a tuple, with the same
    shape/dtypes/structure as ``primals``.

  >>> import jax
  >>>
  >>> f = lambda x, y: 0.5 * x - 0.5 * y
  >>> scalar = jax.ShapeDtypeStruct(shape=(), dtype=np.dtype(np.float32))
  >>> f_transpose = jax.linear_transpose(f, scalar, scalar)
  >>> f_transpose(1.0)
  (Array(0.5, dtype=float32), Array(-0.5, dtype=float32))
  """
  if reduce_axes:
    raise NotImplementedError("reduce_axes argument to transpose is deprecated")
  del reduce_axes
  primals_flat, in_tree = tree_flatten(primals)
  flat_fun, out_tree = flatten_fun_nokwargs(
      lu.wrap_init(fun,
                   debug_info=debug_info("linear_transpose", fun, primals, {})),
      in_tree)
  in_avals = [shaped_abstractify(x) for x in primals_flat]
  in_dtypes = map(lambda a: a.dtype, in_avals)

  in_pvals = map(pe.PartialVal.unknown, in_avals)
  jaxpr, out_pvals, const = pe.trace_to_jaxpr_nounits(flat_fun, in_pvals,
                                                      instantiate=True)
  jaxpr, _ = pe.dce_jaxpr(jaxpr, [True] * len(jaxpr.outvars), True)
  out_avals, _ = unzip2(out_pvals)
  out_dtypes = map(lambda a: a.dtype, out_avals)
  if not (all(dtypes.issubdtype(d, np.inexact) for d in in_dtypes + out_dtypes)
          or all(dtypes.issubdtype(d, np.integer)
                 for d in in_dtypes + out_dtypes)):
    raise TypeError("linear_transpose only supports [float or complex] -> "
                    "[float or complex], and integer -> integer functions, "
                    f"but got {in_dtypes} -> {out_dtypes}.")

  @api_boundary
  def transposed_fun(const, out_cotangent):
    out_cts, out_tree2 = tree_flatten(out_cotangent)
    if out_tree() != out_tree2:
      raise TypeError("cotangent tree does not match function output, "
                      f"expected {out_tree()} but got {out_tree2}")
    if not all(map(core.typecheck, out_avals, out_cts)):
      raise TypeError("cotangent type does not match function output, "
                      f"expected {out_avals} but got {out_cts}")
    dummies = [ad.UndefinedPrimal(a.to_ct_aval()) for a in in_avals]
    in_cts = ad.backward_pass(jaxpr, True, const, dummies, out_cts)
    in_cts = map(ad.instantiate_zeros, in_cts)
    return tree_unflatten(in_tree, in_cts)

  # Ensure that transposed_fun is a PyTree
  return Partial(transposed_fun, const)


def linear_transpose(transpose_rule, cotangent, *args, **kwargs):
  if type(cotangent) is Zero:
    return [Zero(x.aval.to_tangent_aval()) if isinstance(x, UndefinedPrimal)
            else None for x in args]
  else:
    return transpose_rule(cotangent, **kwargs)

