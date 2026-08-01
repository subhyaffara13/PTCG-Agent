
def sincospisquaredhalf(
  x: Array,
) -> tuple[Array, Array]:
  """
  Accurate evaluation of sin(pi * x**2 / 2) and cos(pi * x**2 / 2).

  As based on the sinpi and cospi functions from SciPy, see:
  - https://github.com/scipy/scipy/blob/v1.14.0/scipy/special/special/cephes/trig.h
  """
  x = jnp.abs(x)
  # define s = x % 2, y = x - s, then
  # r = (x * x / 2) % 2
  #   = [(y + s)*(y + s)/2] % 2
  #   = [y*y/2 + s*y + s*s/2] % 2
  #   = [(y*y/2)%2 + (s*y + s*s/2)%2]%2
  #   = [0 + (s*(y+s/2))%2]%2
  #   = [s*(x-s/2)]%2
  s = jnp.fmod(x, 2.0)
  r = jnp.fmod(s * (x - s / 2), 2.0)

  sinpi = jnp.where(
    r < 0.5,
    jnp.sin(np.pi * r),
    jnp.where(
      r > 1.5,
      jnp.sin(np.pi * (r - 2.0)),
      -jnp.sin(np.pi * (r - 1.0)),
    ),
  )
  cospi = jnp.where(
    r == 0.5,
    0.0,
    jnp.where(r < 1.0, -jnp.sin(np.pi * (r - 0.5)), jnp.sin(np.pi * (r - 1.5))),
  )

  return sinpi, cospi

