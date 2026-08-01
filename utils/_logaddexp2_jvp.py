
def _logaddexp2_jvp(primals, tangents):
  x1, x2 = primals
  t1, t2 = tangents
  primal_out = logaddexp2(x1, x2)
  tangent_out = lax.add(lax.mul(t1, lax.exp2(lax.sub(_replace_inf(x1), _replace_inf(primal_out)))),
                        lax.mul(t2, lax.exp2(lax.sub(_replace_inf(x2), _replace_inf(primal_out)))))
  return primal_out, tangent_out

