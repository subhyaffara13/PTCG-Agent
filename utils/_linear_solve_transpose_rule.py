
def _linear_solve_transpose_rule(cotangent, *primals, const_lengths, jaxprs):
  if jaxprs.transpose_solve is None:
    raise TypeError('transpose_solve required for backwards mode automatic '
                    'differentiation of custom_linear_solve')

  params, b = _split_linear_solve_args(primals, const_lengths)
  if any(ad.is_undefined_primal(x) for xs in params for x in xs):
    raise NotImplementedError("open an issue at https://github.com/google/jax !!")
  assert all(ad.is_undefined_primal(x) for x in b)  # TODO(mattjj): why?
  x_cotangent, other_cotangents = split_list(cotangent, [len(b)])
  if any(type(ct) is not ad_util.Zero for ct in other_cotangents):
    raise NotImplementedError("open an issue at https://github.com/google/jax !!")
  del other_cotangents
  x_cotangent_ = _map(ad_util.instantiate, x_cotangent)
  cotangent_b_full = linear_solve_p.bind(
      *_flatten(params.transpose()), *x_cotangent_,
      const_lengths=const_lengths.transpose(), jaxprs=jaxprs.transpose())
  cotangent_b, _ = split_list(cotangent_b_full, [len(b)])
  return [None] * sum(const_lengths) + cotangent_b

