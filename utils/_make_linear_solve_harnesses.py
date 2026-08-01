
def _make_linear_solve_harnesses():

  def linear_solve(a, b, solve, transpose_solve=None, symmetric=False):
    matvec = partial(lax.dot, a, precision=lax.Precision.HIGHEST)
    return lax.custom_linear_solve(matvec, b, solve, transpose_solve, symmetric)

  def explicit_jacobian_solve(matvec, b):
    return lax.stop_gradient(jnp_linalg.solve(api.jacobian(matvec)(b), b))

  def _make_harness(name,
                    *,
                    shape=(4, 4),
                    dtype=np.float32,
                    symmetric=False,
                    solvers=(explicit_jacobian_solve, explicit_jacobian_solve)):
    solve, transpose_solve = solvers
    transpose_solve_name = transpose_solve.__name__ if transpose_solve else None

    def _make_first_argument(rng):
      a = jtu.rand_default(rng)(shape, dtype)
      if symmetric:
        a = a + a.T
      return a

    define(
        lax.linear_solve_p,
        f"{name}_a={jtu.format_shape_dtype_string(shape, dtype)}_b={jtu.format_shape_dtype_string(shape[:-1], dtype)}_solve={solve.__name__}_transposesolve={transpose_solve_name}_{symmetric=}",
        linear_solve, [
            CustomArg(_make_first_argument),
            RandArg(shape[:-1], dtype),
            StaticArg(solve),
            StaticArg(transpose_solve),
            StaticArg(symmetric)
        ],
        shape=shape,
        dtype=dtype,
        solve=solve,
        transpose_solve=transpose_solve,
        symmetric=symmetric)

  for dtype in jtu.dtypes.all_floating:
    if not dtype in [np.float16, dtypes.bfloat16]:
      _make_harness("dtypes", dtype=dtype)
  # Validate symmetricity
  _make_harness("symmetric", symmetric=True)
  # Validate removing transpose_solve
  _make_harness("transpose_solve", solvers=(explicit_jacobian_solve, None))

