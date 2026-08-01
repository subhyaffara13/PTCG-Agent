
def numerical_jvp(f, primals, tangents, eps=EPS):
  delta = scalar_mul(tangents, eps)
  f_pos = f(*add(primals, delta))
  f_neg = f(*sub(primals, delta))
  return scalar_mul(safe_sub(f_pos, f_neg), 0.5 / eps)

