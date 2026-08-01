
def _complex_dtype(dtype, *args, **kwargs):
  return (np.zeros((), dtype) + np.zeros((), np.complex64)).dtype

