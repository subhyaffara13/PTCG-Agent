import re

def _conj_impl(self: ComplexTensor) -> ComplexTensor:
    re, im = split_complex_tensor(self)
    return ComplexTensor(re, torch._neg_view(im))


def _conj_impl(x, **kw):
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    return complex(real(x), -imag(x))
  else:
    return complex(x, _zeros(x))

