
def custom_gradient(fun):
  """Convenience function for defining custom VJP rules (aka custom gradients).

  While the canonical way to define custom VJP rules is via ``jax.custom_vjp``,
  the ``custom_gradient`` convenience wrapper follows TensorFlow's
  ``tf.custom_gradient`` API. The difference here is that ``custom_gradient``
  can be used as a decorator on one function that returns both the primal value
  (representing the output of the mathematical function to be differentiated)
  and the VJP (gradient) function. See
  https://www.tensorflow.org/api_docs/python/tf/custom_gradient.

  If the mathematical function to be differentiated has Haskell-like signature
  ``a -> b``, then the Python callable ``fun`` should have the signature
  ``a -> (b, CT b --o CT a)`` where we use ``CT x`` to denote a cotangent type
  for ``x`` and the ``--o`` arrow to denote a linear function. See the example
  below. That is, ``fun`` should return a pair where the first element
  represents the value of the mathematical function to be differentiated and the
  second element is a function to be called on the backward pass of reverse-mode
  automatic differentiation (i.e. the "custom gradient" function).

  The function returned as the second element of the output of ``fun`` can close
  over intermediate values computed when evaluating the function to be
  differentiated. That is, use lexical closure to share work between the forward
  pass and the backward pass of reverse-mode automatic differentiation. However,
  it cannot perform Python control flow which depends on the values of the
  closed-over intermediate values or its cotangent arguments; if the function
  includes such control flow, an error is raised.

  Args:
    fun: a Python callable specifying both the mathematical function to be
      differentiated and its reverse-mode differentiation rule. It should return
      a pair consisting of an output value and a Python callable that represents
      the custom gradient function.

  Returns:
    A Python callable that accepts the same arguments as ``fun`` and returns the
    output value specified by the first element of ``fun``'s output pair.

  For example:

  >>> @jax.custom_gradient
  ... def f(x):
  ...   return x ** 2, lambda g: (g * x,)
  ...
  >>> print(f(3.))
  9.0
  >>> print(jax.grad(f)(3.))
  3.0

  An example with a function on two arguments, so that the VJP function must
  return a tuple of length two:

  >>> @jax.custom_gradient
  ... def f(x, y):
  ...   return x * y, lambda g: (g * y, g * x)
  ...
  >>> print(f(3., 4.))
  12.0
  >>> print(jax.grad(f, argnums=(0, 1))(3., 4.))
  (Array(4., dtype=float32, weak_type=True), Array(3., dtype=float32, weak_type=True))
  """
  @custom_vjp
  def wrapped_fun(*args, **kwargs):
    ans, _ = fun(*args, **kwargs)
    return ans

  def fwd(*args, **kwargs):
    ans, rule = fun(*args, **kwargs)
    ans_flat, out_tree = tree_flatten((ans,))
    debug_fwd = debug_info("custom_gradient fwd", rule, (ans,), {})
    rule, in_tree = flatten_fun_nokwargs(lu.wrap_init(rule,
                                                      debug_info=debug_fwd), out_tree)
    ans_avals = [core.typeof(x).to_ct_aval() for x in ans_flat]
    jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(rule, ans_avals)
    return ans, Residuals(jaxpr, in_tree(), out_tree, consts)

  def bwd(res, cts):
    jaxpr, in_tree, out_tree, consts = res
    cts_flat, out_tree_ = tree_flatten((cts,))
    if out_tree != out_tree_: raise TypeError(f'{out_tree}\n!=\n{out_tree_}')
    cts_out = core.eval_jaxpr(jaxpr, consts, *cts_flat)
    cts_out = tree_unflatten(in_tree, cts_out)
    if treedef_is_leaf(in_tree):
      cts_out = (cts_out,)
    return cts_out

  wrapped_fun.defvjp(fwd, bwd)
  return wrapped_fun

