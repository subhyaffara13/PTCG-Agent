
def _norm_logpdf(x):
    return -x**2 / 2.0 - _norm_pdf_logC


def _norm_logpdf(x):
  neg_half = _lax_const(x, -0.5)
  log_normalizer = _lax_const(x, _norm_logpdf_constant)
  return lax.sub(lax.mul(neg_half, lax.square(x)), log_normalizer)

