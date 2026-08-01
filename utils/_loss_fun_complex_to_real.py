
def _loss_fun_complex_to_real(z):
  return (z.conj() * z).real.sum()

