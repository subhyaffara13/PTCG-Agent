
def _sici_series(x: Array):
  # sici series valid for x >= 0 and x <= 4
  def si_series(x):
    # Values come from Cephes Implementation used by Scipy https://github.com/jeremybarnes/cephes/blob/60f27df395b8322c2da22c83751a2366b82d50d1/misc/sici.c
    SN = np.array([-8.39167827910303881427E-11,
      4.62591714427012837309E-8,
      -9.75759303843632795789E-6,
      9.76945438170435310816E-4,
      -4.13470316229406538752E-2,
      1.00000000000000000302E0], dtype=x.dtype)
    SD = np.array([ 2.03269266195951942049E-12,
      1.27997891179943299903E-9,
      4.41827842801218905784E-7,
      9.96412122043875552487E-5,
      1.42085239326149893930E-2,
      9.99999999999999996984E-1], dtype=x.dtype)
    t = x * x
    return (x * jnp.polyval(SN, t)) / jnp.polyval(SD, t)

  def ci_series(x):
    # Values come from Cephes Implementation used by Scipy https://github.com/jeremybarnes/cephes/blob/60f27df395b8322c2da22c83751a2366b82d50d1/misc/sici.c
    CN = np.array([ 2.02524002389102268789E-11,
      -1.35249504915790756375E-8,
      3.59325051419993077021E-6,
      -4.74007206873407909465E-4,
      2.89159652607555242092E-2,
      -1.00000000000000000080E0], dtype=x.dtype)
    CD = np.array([ 4.07746040061880559506E-12,
      3.06780997581887812692E-9,
      1.23210355685883423679E-6,
      3.17442024775032769882E-4,
      5.10028056236446052392E-2,
      4.00000000000000000080E0], dtype=x.dtype)
    t = x * x
    return np.euler_gamma + jnp.log(x) + t * jnp.polyval(CN, t) / jnp.polyval(CD, t)

  si = jnp.where(
    x == 0,
    0.0,
    si_series(x)
  )

  ci = jnp.where(
    x == 0,
    -np.inf,
    ci_series(x)
  )

  return si, ci

