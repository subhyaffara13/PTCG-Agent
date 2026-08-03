from typing import Any, Callable

def linearize(
    func: Callable[..., Any], *primals: Any
) -> tuple[Any, Callable[..., Any]]:
    """
    Returns the value of ``func`` at ``primals`` and linear approximation
    at ``primals``.

    Args:
        func (Callable[..., Any]): A Python function that takes one or more arguments.
        primals (Tensors): Positional arguments to ``func`` that must all be
            Tensors. These are the values at which the function is linearly approximated.

    Returns:
        Returns a ``(output, jvp_fn)`` tuple containing the output of ``func``
        applied to ``primals`` and a function that computes the jvp of
        ``func`` evaluated at ``primals``.

    linearize is useful if jvp is to be computed multiple times at ``primals``. However,
    to achieve this, linearize saves intermediate computation and has higher memory requirements
    than directly applying `jvp`. So, if all the ``tangents`` are known, it maybe more efficient
    to compute vmap(jvp) instead of using linearize.

    .. note::
        linearize evaluates ``func`` twice. Please file an issue for an implementation
        with a single evaluation.

    Example::

        >>> import torch
        >>> from torch.func import linearize
        >>> def fn(x):
        ...     return x.sin()
        ...
        >>> output, jvp_fn = linearize(fn, torch.zeros(3, 3))
        >>> jvp_fn(torch.ones(3, 3))
        tensor([[1., 1., 1.],
                [1., 1., 1.],
                [1., 1., 1.]])
        >>>

    """
    # Note: We evaluate `fn` twice.
    # Once for returning the output and other while
    # tracing the graph.
    # If this becomes a bottle-neck, we should update
    # make_fx such that it also returns the output.

    output = func(*primals)
    _, output_spec = tree_flatten(output)

    flat_primals, primals_argspec = tree_flatten(primals)

    # tangents for tracing
    flat_tangents = tuple(p.new_empty(()).expand_as(p) for p in flat_primals)

    # function to trace
    def trace_fn(flat_tangents: tuple[torch.Tensor, ...]) -> Any:
        with fwAD.dual_level():
            flat_duals = tuple(
                fwAD.make_dual(p, t) for p, t in zip(flat_primals, flat_tangents)
            )
            duals = tree_unflatten(flat_duals, primals_argspec)
            output = func(*duals)
            tangents = tree_map_only(
                torch.Tensor, lambda dual: safe_unpack_dual(dual, False)[1], output
            )

        return tangents

    jvp_graph = lazy_dynamo_disallow(make_fx)(trace_fn)(flat_tangents)
    const_folded_jvp_graph = lazy_dynamo_disallow(const_fold.split_const_subgraphs)(
        jvp_graph
    )

    # Hold only the meta-data regarding the primals.
    flat_primals_shape = tuple(p.shape for p in flat_primals)
    flat_primals_device = tuple(p.device for p in flat_primals)
    flat_primals_dtype = tuple(p.dtype for p in flat_primals)

    def forward_ad_checks(flat_tangents: Sequence[torch.Tensor]) -> None:
        for idx, t in enumerate(flat_tangents):
            if t.shape != flat_primals_shape[idx]:
                msg = (
                    f"tangent:{idx} with shape {t.shape} in flattened "
                    f"pytree doesn't match the shape {flat_primals_shape[idx]} "
                    "of the corresponding primal."
                )
                raise RuntimeError(msg)

            if t.device != flat_primals_device[idx]:
                msg = (
                    f"tangent:{idx} with device {t.device} in flattened "
                    f"pytree doesn't match the device {flat_primals_device[idx]} "
                    "of the corresponding primal."
                )
                raise RuntimeError(msg)

            if t.dtype != flat_primals_dtype[idx]:
                msg = (
                    f"tangent:{idx} with dtype {t.dtype} in flattened "
                    f"pytree doesn't match the dtype {flat_primals_dtype[idx]} "
                    "of the corresponding primal."
                )
                raise RuntimeError(msg)

    # jvp_fn : Callable[..., Any] to return
    #   It takes care of checking the argspec of tangents,
    #   calling the folded fx graph and unflattening fx graph output
    def jvp_fn(*tangents: Any) -> Any:
        flat_tangents, tangent_argspec = tree_flatten(tangents)
        if tangent_argspec != primals_argspec:
            raise RuntimeError(
                f"Expected the tangents {tangent_argspec} to have "
                f"the same argspec as the primals {primals_argspec}"
            )

        forward_ad_checks(flat_tangents)  # type: ignore[arg-type]

        flat_output = const_folded_jvp_graph(*flat_tangents)
        # const folded graph can return flat output,
        # so transform output.
        return tree_unflatten(flat_output, output_spec)

    return output, jvp_fn


def linearize(fun: Callable, *primals, has_aux: Literal[False] = False
              ) -> tuple[Any, Callable]:
  ...


def linearize(fun: Callable, *primals, has_aux: Literal[True]
              ) -> tuple[Any, Callable, Any]:
  ...


def linearize(fun: Callable, *primals, has_aux: bool = False
              ) -> tuple[Any, Callable] | tuple[Any, Callable, Any]:
  """Produces a linear approximation to ``fun`` using :py:func:`jvp` and partial eval.

  Args:
    fun: Function to be differentiated. Its arguments should be arrays, scalars,
      or standard Python containers of arrays or scalars. It should return an
      array, scalar, or standard python container of arrays or scalars.
    primals: The primal values at which the Jacobian of ``fun`` should be
      evaluated. Should be a tuple of arrays, scalar, or standard Python
      container thereof. The length of the tuple is equal to the number of
      positional parameters of ``fun``.
    has_aux: Optional, bool. Indicates whether ``fun`` returns a pair where the first
      element is considered the output of the mathematical function to be linearized,
      and the second is auxiliary data. Default False.

  Returns:
    If ``has_aux`` is ``False``, returns a pair where the first element is the value of
    ``f(*primals)`` and the second element is a function that evaluates the
    (forward-mode) Jacobian-vector product of ``fun`` evaluated at ``primals`` without
    re-doing the linearization work. If ``has_aux`` is ``True``, returns a
    ``(primals_out, lin_fn, aux)`` tuple where ``aux`` is the auxiliary data returned by
    ``fun``.

  In terms of values computed, :py:func:`linearize` behaves much like a curried
  :py:func:`jvp`, where these two code blocks compute the same values::

    y, out_tangent = jax.jvp(f, (x,), (in_tangent,))

    y, f_jvp = jax.linearize(f, x)
    out_tangent = f_jvp(in_tangent)

  However, the difference is that :py:func:`linearize` uses partial evaluation
  so that the function ``f`` is not re-linearized on calls to ``f_jvp``. In
  general that means the memory usage scales with the size of the computation,
  much like in reverse-mode. (Indeed, :py:func:`linearize` has a similar
  signature to :py:func:`vjp`!)

  This function is mainly useful if you want to apply ``f_jvp`` multiple times,
  i.e. to evaluate a pushforward for many different input tangent vectors at the
  same linearization point. Moreover if all the input tangent vectors are known
  at once, it can be more efficient to vectorize using :py:func:`vmap`, as in::

    pushfwd = partial(jvp, f, (x,))
    y, out_tangents = vmap(pushfwd, out_axes=(None, 0))((in_tangents,))

  By using :py:func:`vmap` and :py:func:`jvp` together like this we avoid the stored-linearization
  memory cost that scales with the depth of the computation, which is incurred
  by both :py:func:`linearize` and :py:func:`vjp`.

  Here's a more complete example of using :py:func:`linearize`:

  >>> import jax
  >>> import jax.numpy as jnp
  >>>
  >>> def f(x): return 3. * jnp.sin(x) + jnp.cos(x / 2.)
  ...
  >>> jax.jvp(f, (2.,), (3.,))
  (Array(3.2681944, dtype=float32, weak_type=True), Array(-5.007528, dtype=float32, weak_type=True))
  >>> y, f_jvp = jax.linearize(f, 2.)
  >>> print(y)
  3.2681944
  >>> print(f_jvp(3.))
  -5.007528
  >>> print(f_jvp(4.))
  -6.676704
  """
  check_callable(fun)
  primals_ft = FlatTree.flatten(primals)
  out_primals_ft, out_known, jaxpr, consts, *maybe_aux = ad.linearize(
      fun, primals_ft, has_aux=has_aux)
  in_avals = primals_ft.map(core.typeof)
  out_avals = out_primals_ft.map(core.typeof)
  lifted_jvp = Partial(
      partial(_lift_linearized, jaxpr, in_avals, out_avals, out_known), consts)
  return out_primals_ft.unflatten(), lifted_jvp, *maybe_aux


def linearize(traceable, primals_ft, has_aux=False, is_vjp=False):
  dbg = debug_info("linearize", traceable, primals_ft, {})
  tag = core.TraceTag()
  with core.take_current_trace() as parent_trace:
    source_info = source_info_util.current()
    tangent_trace = pe.DynamicJaxprTrace(dbg, auto_dce=True)
    tangent_trace.tag = tag
    lin_trace = LinearizeTrace(parent_trace, tangent_trace, is_vjp)
    def make_tracer(_lin_trace, p):
      t = tangent_trace.new_arg(typeof(p).to_tangent_aval(), source_info)
      if (not isinstance(t, Zero)
          and isinstance(typeof(t), core.ShapedArray)
          and dtype(t) == float0):
        t = p2tz(t)
      return LinearizeTracer(_lin_trace, p, t).full_lower()
    tracers = primals_ft.map(partial(make_tracer, lin_trace))

    with (core.set_current_trace(lin_trace),
          source_info_util.transform_name_stack('jvp')):
      ans = traceable(*tracers.unflatten())
      if has_aux:
        if not isinstance(ans, (list, tuple)) or len(ans) != 2:
          raise TypeError("expected function with aux output to return a two-element "
                          f"tuple, but got type {type(ans)} with value {ans!r}")
        ans, aux = ans
        auxs = ft.flatten(aux).map(partial(_strip_tracer, LinearizeTracer, tag)),
      else:
        auxs = ()
      out_primals, out_tangents = ft.flatten(ans).map(
          lin_trace.to_primal_tangent_pair).unzip2()
      del lin_trace, ans, tracers
  out_nzs = [type(t) is not Zero for t in out_tangents]
  out_nz_tangents = [t for t, nz in zip(out_tangents, out_nzs) if nz]
  out_nz_tangents = map(partial(tangent_trace.to_jaxpr_tracer,
                                source_info=source_info), out_nz_tangents)
  dbg = dbg.with_unknown_names()
  jaxpr, consts = tangent_trace.to_jaxpr(out_nz_tangents, dbg, source_info)
  tangent_trace.invalidate()
  config.enable_checks.value and core.check_jaxpr(jaxpr)
  jaxpr, used_consts, _ = pe.dce_jaxpr_consts(
      jaxpr, [True] * len(jaxpr.outvars),
      [False] * len(jaxpr.constvars) + [True] * len(jaxpr.invars))
  consts = [c for c, used in zip(consts, used_consts) if used]
  out_zeros = map(op.not_, out_nzs)
  auxs = tuple(aux.unflatten() for aux in auxs)
  return out_primals, out_zeros, jaxpr, consts, *auxs

