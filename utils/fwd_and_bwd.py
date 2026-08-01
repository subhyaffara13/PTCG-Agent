
def fwd_and_bwd(
    fun: Callable, argnums: int | Sequence[int], has_aux: bool = False,
    jitted: bool = True,
) -> tuple[Callable, Callable]:
  """Creates functions ``fwd`` and ``bwd`` corresponding to the forward and
  backward pass of a given function ``fun``. The forward function ``fwd(*args)``
  functionally behaves much like ``y, fun_vjp = jax.vjp(fun, *args)``, but allows
  reuse of the backward function ``bwd`` across multiple iterations, which is
  useful to avoid recompilation when the forward and backward do not end up in a
  single jitted function:

  >>> import jax
  >>>
  >>> x = W = cot_out = jax.numpy.ones((4,4))
  >>>
  >>> def f(x, W):
  ...     return x @ W
  ...
  >>> f_jitted = jax.jit(f)
  >>> for i in range(3):
  ...     y, f_vjp = jax.vjp(f_jitted, x, W)
  ...     cot_x, cot_W = f_vjp(cot_out)           # not jitted
  ...     cot_x, cot_W = jax.jit(f_vjp)(cot_out)  # recompiles on every iteration
  ...
  >>> fwd, bwd = jax.fwd_and_bwd(f, argnums=(0,1))
  >>> for i in range(3):
  ...     y, residuals = fwd(x, W)
  ...     cot_x, cot_W = bwd(residuals, cot_out)  # jitted, compiles once
  ...

  Args:
    fun: Function to produce a forward and backward of.
    argnums: Integer or sequence of integers. Specifies which positional argument(s)
      to differentiate with respect to.
    has_aux: Optional, bool. Indicates whether ``fun`` returns a pair where the
     first element is considered the output of the mathematical function to be
     differentiated and the second element is auxiliary data. Default False.
    jitted: Optional, bool. Indicates whether to return the ``jax.jit`` of
      forward and backward. Note that jit-ing only the backward but not the
      forward will result in the backward recompiling on every invocation, so we
      default to jit-ing both.

  Returns:
    The two functions, ``fwd`` and ``bwd``.

    If ``has_aux`` is ``False``, ``fwd(*primals)`` returns a tuple
    ``(primals_out, residuals)``, where ``primals_out`` is ``fun(*primals)``.
    If ``has_aux`` is ``True``, returns a ``(primals_out, residuals, aux)`` tuple
    where ``aux`` is the auxiliary data returned by ``fun``.

    ``bwd`` is a function from ``residuals`` and a cotangent vector with the same
    shape as ``primals_out`` to a tuple of cotangent vectors with the same number
    and shapes as the ``primals`` designated by ``argnums``, representing the
    vector-Jacobian product of ``fun`` evaluated at ``primals``.
  """
  check_callable(fun)
  argnums = _ensure_index(argnums)

  def fwd(*args, **kwargs):
    f_partial, dyn_args = argnums_partial2(fun, argnums, args, {})
    return vjp(f_partial, *dyn_args, has_aux=has_aux)
  def bwd(f_vjp, outgrad):
    g = f_vjp(outgrad)
    g = g[0] if isinstance(argnums, int) else g
    return g
  if jitted:
    fwd = jit(fwd)
    bwd = jit(bwd)
  return fwd, bwd

