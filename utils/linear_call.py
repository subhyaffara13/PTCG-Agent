from typing import Callable

def linear_call(fun: Callable,
                fun_transpose: Callable, residual_args,
                linear_args):
  """Call a linear function, with a custom implementation for its transpose.

  The `Haskell-like type signatures`_ of ``fun`` and ``fun_transpose`` are:

  .. code-block:: haskell

    fun           :: r -> a -o b
    fun_transpose :: r -> b -o a

  where the ``-o`` arrow indicates a linear function, ``r`` is the
  residual input type and ``a`` is the linear input type.

  The functions ``fun`` and ``fun_transpose`` are coupled as
  transposes of one another. Specifically, the transpose of a
  ``linear_call`` primitive is another ``linear_call`` to
  ``fun_transpose``, with ``fun`` as its custom transposition.

  For example:

  >>> def f(r, x):
  ...   return x / r

  >>> def t(r, t):
  ...   return t / r

  >>> def div_add(x, denom):
  ...   return x + linear_call(f, t, denom, x)

  >>> def transpose(f, x_example):
  ...   def transposed(y):
  ...     x, = jax.linear_transpose(f, x_example)(y)
  ...     return x
  ...   return transposed

  >>> div_add(9., 3.)
  Array(12., dtype=float32, weak_type=True)

  >>> transpose(partial(div_add, denom=3.), 1.)(18.)  # custom
  Array(24., dtype=float32, weak_type=True)

  >>> transpose(lambda x: x + x / 3., 1.)(18.)  # reference
  Array(24., dtype=float32, weak_type=True)

  The above definition of ``f`` illustrates the purpose of a residual
  argument: division is linear in one of its inputs (the dividend
  ``x``) but not the other (the divisor ``r``).

  As another example:

  >>> def custom_id(x):
  ...   def f(_, x): return x
  ...   def t(_, t): return 7.
  ...   return linear_call(f, t, (), x)
  >>> custom_id(1.)
  TypedFloat(1.0, dtype=float32)
  >>> transpose(custom_id, 1.)(1.)
  TypedFloat(7.0, dtype=float32)
  >>> transpose(transpose(custom_id, 1.), 1.)(1.)
  TypedFloat(1.0, dtype=float32)
  >>> transpose(transpose(transpose(custom_id, 1.), 1.), 1.)(1.)
  TypedFloat(7.0, dtype=float32)

  Args:
    fun: a Python callable specifying a linear function. It should
      take two arguments: one of "residual" inputs (type ``r``),
      i.e. inputs in which the function is not necessarily linear, and
      one of "linear" inputs (type ``a``).  It should return output
      whose components are linear in the linear input (type ``b``).
    fun_transpose: a Python callable specifying a structurally linear
      function that is the transpose of ``fun`` with respect to its
      linear inputs. Its first argument is the same residual inputs
      (``r``) as ``fun``. Its second argument is of type
      ``b``. Finally, its output is of type ``a`` and each of its
      component are linear in its second argument (the ``b`` inputs).
    residual_args: Argument in which ``fun`` and ``fun_transpose`` are
      not necessarily linear. Not involved in transposition.
    linear_args: Argument in which ``fun`` and ``fun_transpose`` are
      linear and with respect to which the two are transposes.

  Returns:
    The call result, i.e. ``fun(residual_args, linear_args)``.

  .. _Haskell-like type signatures: https://wiki.haskell.org/Type_signature
  """
  operands_res, res_tree = tree_flatten(residual_args)
  operands_lin, lin_tree = tree_flatten(linear_args)

  f_in_tree = treedef_tuple((res_tree, lin_tree))
  f, out_tree = flatten_fun_nokwargs(
      lu.wrap_init(
          fun,
          debug_info=debug_info("linear_call fun", fun,
                                (residual_args, linear_args), {})),
      f_in_tree)

  res_avals = map(core.typeof, operands_res)
  lin_avals = map(core.typeof, operands_lin)
  f_jaxpr, f_consts = _initial_style_jaxpr(f, (*res_avals, *lin_avals))
  f_jaxpr_closed = _close_jaxpr(f_jaxpr)
  out_avals = f_jaxpr_closed.out_avals

  t_in_tree = treedef_tuple((res_tree, out_tree()))
  t, t_out_tree = flatten_fun_nokwargs(
      lu.wrap_init(
          fun_transpose,
          # TODO(necula): the fun_transpose takes residual and output of fun!
          debug_info=debug_info("linear_call fun_transpose", fun_transpose,
                                (residual_args, linear_args), {})),
      t_in_tree)

  @pe._memoize
  def transpose_thunk():
    t_jaxpr, t_consts = _initial_style_jaxpr(t.with_unknown_names(),
                                             (*res_avals, *out_avals))
    if t_out_tree() != lin_tree:
      raise TypeError(
          'transpose output pytree structure must match that of linear inputs, '
          f'got output structure {t_out_tree()} '
          f'and input structure {lin_tree}.')
    return _close_jaxpr(t_jaxpr), t_consts

  out = linear_call_p.bind(*f_consts, *operands_res, *operands_lin,
                           callee=f_jaxpr_closed,
                           transpose_thunk=transpose_thunk,
                           num_callee_consts=len(f_consts),
                           num_res=len(operands_res))

  return tree_unflatten(out_tree(), out)

