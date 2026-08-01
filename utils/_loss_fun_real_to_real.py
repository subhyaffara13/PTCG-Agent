
def _loss_fun_real_to_real(params):
  x, y = params
  return _loss_fun_complex_to_real(x + y * 1j)

