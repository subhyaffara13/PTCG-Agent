
def _make_triangular_solve_harness(name,
                                   *,
                                   left_side=True,
                                   lower=False,
                                   ab_shapes=((4, 4), (4, 1)),
                                   dtype=np.float32,
                                   transpose_a=False,
                                   conjugate_a=False,
                                   unit_diagonal=False):
  a_shape, b_shape = ab_shapes
  f_lax = lambda a, b: (
      lax.linalg.triangular_solve_p.bind(
          a,
          b,
          left_side=left_side,
          lower=lower,
          transpose_a=transpose_a,
          conjugate_a=conjugate_a,
          unit_diagonal=unit_diagonal))

  define(
      lax.linalg.triangular_solve_p,
      f"{name}_a={jtu.format_shape_dtype_string(a_shape, dtype)}_b={jtu.format_shape_dtype_string(b_shape, dtype)}_leftside={left_side}_{lower=}_transposea={transpose_a}_conjugatea={conjugate_a}_unitdiagonal={unit_diagonal}",
      f_lax, [RandArg(a_shape, dtype),
              RandArg(b_shape, dtype)],
      jax_unimplemented=[
          Limitation("unimplemented", devices="gpu", dtypes=[np.float16]),
      ],
      dtype=dtype,
      a_shape=a_shape,
      b_shape=b_shape,
      left_side=left_side,
      lower=lower,
      tranpose_a=transpose_a,
      conjugate_a=conjugate_a,
      unit_diagonal=unit_diagonal)

