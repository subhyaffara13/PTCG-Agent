
def abs2(x):
  if jnp.iscomplexobj(x):
    return x.real ** 2 + x.imag ** 2
  else:
    return x ** 2

