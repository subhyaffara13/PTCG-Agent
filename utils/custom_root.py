from typing import Any, Callable

def custom_root(f: Callable,
                initial_guess: Any,
                solve: Callable[[Callable, Any], Any],
                tangent_solve: Callable[[Callable, Any], Any],
                has_aux=False):
  """Differentiably solve for the roots of a function.

  This is a low-level routine, mostly intended for internal use in JAX.
  Gradients of custom_root() are defined with respect to closed-over variables
  from the provided function ``f`` via the implicit function theorem:
  https://en.wikipedia.org/wiki/Implicit_function_theorem

  Args:
    f: function for which to find a root. Should accept a single argument,
      return a tree of arrays with the same structure as its input.
    initial_guess: initial guess for a zero of f.
    solve: function to solve for the roots of f. Should take two positional
      arguments, f and initial_guess, and return a solution with the same
      structure as initial_guess such that func(solution) = 0. In other words,
      the following is assumed to be true (but not checked)::

        solution = solve(f, initial_guess)
        error = f(solution)
        assert all(error == 0)

    tangent_solve: function to solve the tangent system. Should take two
      positional arguments, a linear function ``g`` (the function ``f``
      linearized at its root) and a tree of array(s) ``y`` with the same
      structure as initial_guess, and return a solution ``x`` such that
      ``g(x)=y``:

      - For scalar ``y``, use ``lambda g, y: y / g(1.0)``.
      - For vector ``y``, you could use a linear solve with the Jacobian, if
        dimensionality of ``y`` is not too large:
        ``lambda g, y: np.linalg.solve(jacobian(g)(y), y)``.
    has_aux: bool indicating whether the ``solve`` function returns
      auxiliary data like solver diagnostics as a second argument.

  Returns:
    The result of calling solve(f, initial_guess) with gradients defined via
    implicit differentiation assuming ``f(solve(f, initial_guess)) == 0``.
  """
  guess_flat = FlatTree.flatten(initial_guess)
  guess_avals = guess_flat.map(core.typeof)
  f_debug = api_util.debug_info("custom_root", f, (initial_guess,), {})
  args_avals = FlatTree.pack(((guess_avals,),{}))
  f_jaxpr, out_avals = pe.trace_to_jaxpr(f, args_avals, f_debug)
  f_jaxpr, f_consts = pe.separate_consts(f_jaxpr)

  _check_tree("f", "initial_guess", out_avals.tree, guess_avals.tree, False)

  solve_debug = api_util.debug_info("custom_root solve", solve,
                                    (f, initial_guess), {},
                                    static_argnums=(0,))
  solve_jaxpr, solution_avals = pe.trace_to_jaxpr(
      partial(solve, f), args_avals, solve_debug)
  solve_jaxpr, solve_consts = pe.separate_consts(solve_jaxpr)
  _check_tree("solve", "initial_guess", solution_avals.tree, guess_flat.tree, has_aux)

  def linearize_and_solve(x, b):
    unchecked_zeros, f_jvp = api.linearize(f, x)
    return tangent_solve(f_jvp, b)

  linearize_and_solve_dbg = api_util.debug_info("custom_root tangent_solve",
      tangent_solve, (initial_guess, initial_guess), {})


  linearize_and_solve_avals = FlatTree.pack(((guess_avals, guess_avals), {}))
  l_and_s_jaxpr, out_avals = pe.trace_to_jaxpr(
      linearize_and_solve, linearize_and_solve_avals, linearize_and_solve_dbg)
  l_and_s_jaxpr, l_and_s_consts = pe.separate_consts(l_and_s_jaxpr)
  _check_tree("tangent_solve", "x", out_avals.tree, guess_flat.tree, False)

  all_consts = [f_consts, solve_consts, l_and_s_consts]
  const_lengths = _RootTuple(*_map(len, all_consts))
  jaxprs = _RootTuple(f_jaxpr, solve_jaxpr, l_and_s_jaxpr)

  solution_flat = _custom_root(
      const_lengths, jaxprs, *_flatten(all_consts), *guess_flat)
  return solution_avals.update(solution_flat).unflatten()

