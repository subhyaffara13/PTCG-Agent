from typing import Any, Callable

def custom_linear_solve(
    matvec: Callable,
    b: Any,
    solve: Callable[[Callable, Any], Any],
    transpose_solve: Callable[[Callable, Any], Any] | None = None,
    symmetric=False, has_aux=False):
  """Perform a matrix-free linear solve with implicitly defined gradients.

  This function allows for overriding or defining gradients for a linear
  solve directly via implicit differentiation at the solution, rather than by
  differentiating *through* the solve operation. This can sometimes be much faster
  or more numerically stable, or differentiating through the solve operation
  may not even be implemented (e.g., if ``solve`` uses ``lax.while_loop``).

  Required invariant::

      x = solve(matvec, b)  # solve the linear equation
      assert matvec(x) == b  # not checked

  Args:
    matvec: linear function to invert. Must be differentiable.
    b: constant right handle side of the equation. May be any nested structure
      of arrays.
    solve: higher level function that solves for solution to the linear
      equation, i.e., ``solve(matvec, x) == x`` for all ``x`` of the same form
      as ``b``. This function need not be differentiable.
    transpose_solve: higher level function for solving the transpose linear
      equation, i.e., ``transpose_solve(vecmat, x) == x``, where ``vecmat`` is
      the transpose of the linear map ``matvec`` (computed automatically with
      autodiff). Required for backwards mode automatic differentiation, unless
      ``symmetric=True``, in which case ``solve`` provides the default value.
    symmetric: bool indicating if it is safe to assume the linear map
      corresponds to a symmetric matrix, i.e., ``matvec == vecmat``.
    has_aux: bool indicating whether the ``solve`` and ``transpose_solve`` functions
      return auxiliary data like solver diagnostics as a second argument.

  Returns:
    Result of ``solve(matvec, b)``, with gradients defined assuming that the
      solution ``x`` satisfies the linear equation ``matvec(x) == b``.
  """
  if transpose_solve is None and symmetric:
    transpose_solve = solve

  b_flat = FlatTree.flatten(b)
  b_avals = b_flat.map(core.typeof)
  tree = b_flat.tree

  def _shape_checked(fun, name, has_aux):
    def f(x):
      y = fun(x)
      _check_shapes(name, "b", tree_leaves(y), b_flat)
      return y

    def f_aux(x):
      y, aux = fun(x)
      _check_shapes(name, "b", tree_leaves(y), b_flat)
      return y, aux

    return f_aux if has_aux else f

  matvec_debug = api_util.debug_info("custom_linear_solve",
                                     matvec, (b,), {})
  # no auxiliary data assumed for matvec
  args_avals = FlatTree.pack(((b_avals,),{}))
  matvec_jaxpr, out_avals = pe.trace_to_jaxpr(
      _shape_checked(matvec, "matvec", False), args_avals,
      matvec_debug)
  matvec_jaxpr, matvec_consts = pe.separate_consts(matvec_jaxpr)
  _check_tree("matvec", "b", out_avals.tree, tree, False)

  solve_debug = api_util.debug_info("custom_linear_solve solve",
                                    solve, (matvec, b), {},
                                    static_argnums=(0,))
  solve_jaxpr, out_avals = pe.trace_to_jaxpr(
      _shape_checked(partial(solve, matvec), "solve", has_aux), args_avals,
      solve_debug)
  solve_jaxpr, solve_consts = pe.separate_consts(solve_jaxpr)
  _check_tree("solve", "b", out_avals.tree, tree, has_aux)

  if transpose_solve is None:
    vecmat_jaxpr = tr_solve_jaxpr = None
    vecmat_consts = tr_solve_consts = []
  else:
    transpose_solve_debug = api_util.debug_info(
        "custom_linear_solve transpose_solve", transpose_solve,
        (matvec, b), {}, static_argnums=(0,))
    if symmetric:
      vecmat = matvec
      vecmat_jaxpr = matvec_jaxpr
      vecmat_consts = matvec_consts
    else:
      vecmat = _transpose_one_output(matvec, b)
      vecmat_jaxpr, out_avals = pe.trace_to_jaxpr(
          vecmat, args_avals, transpose_solve_debug)
      vecmat_jaxpr, vecmat_consts = pe.separate_consts(vecmat_jaxpr)
      assert out_avals.tree == tree

    tr_solve_jaxpr, out_avals = pe.trace_to_jaxpr(
        _shape_checked(partial(transpose_solve, vecmat), "transpose_solve", has_aux),
        args_avals, transpose_solve_debug)
    tr_solve_jaxpr, tr_solve_consts = pe.separate_consts(tr_solve_jaxpr)
    _check_tree("transpose_solve", "b", out_avals.tree, tree, has_aux)

  all_consts = [matvec_consts, vecmat_consts, solve_consts, tr_solve_consts]
  const_lengths = _LinearSolveTuple(*_map(len, all_consts))
  jaxprs = _LinearSolveTuple(
      matvec_jaxpr, vecmat_jaxpr, solve_jaxpr, tr_solve_jaxpr)

  args = _flatten(all_consts) + list(b_flat)
  args = core.auto_insert_reshard(*args)
  out_flat = linear_solve_p.bind(*args, const_lengths=const_lengths, jaxprs=jaxprs)

  return out_avals.update(out_flat).unflatten()

