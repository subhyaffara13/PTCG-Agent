
def _ndtri(p: ArrayLike) -> Array:
  """Implements ndtri core logic."""
  dtype = lax.dtype(p).type
  shape = np.shape(p)

  # Constants used in piece-wise rational approximations. Taken from the cephes
  # library:
  # https://root.cern.ch/doc/v608/SpecFuncCephesInv_8cxx_source.html
  p0 = np.array([-5.99633501014107895267E1,
                 9.80010754185999661536E1,
                 -5.66762857469070293439E1,
                 1.39312609387279679503E1,
                 -1.23916583867381258016E0], dtype=dtype)
  q0 = np.array([1.0,
                 1.95448858338141759834E0,
                 4.67627912898881538453E0,
                 8.63602421390890590575E1,
                 -2.25462687854119370527E2,
                 2.00260212380060660359E2,
                 -8.20372256168333339912E1,
                 1.59056225126211695515E1,
                 -1.18331621121330003142E0], dtype=dtype)
  p1 = np.array([4.05544892305962419923E0,
                 3.15251094599893866154E1,
                 5.71628192246421288162E1,
                 4.40805073893200834700E1,
                 1.46849561928858024014E1,
                 2.18663306850790267539E0,
                 -1.40256079171354495875E-1,
                 -3.50424626827848203418E-2,
                 -8.57456785154685413611E-4], dtype=dtype)
  q1 = np.array([1.0,
                 1.57799883256466749731E1,
                 4.53907635128879210584E1,
                 4.13172038254672030440E1,
                 1.50425385692907503408E1,
                 2.50464946208309415979E0,
                 -1.42182922854787788574E-1,
                 -3.80806407691578277194E-2,
                 -9.33259480895457427372E-4], dtype=dtype)
  p2 = np.array([3.23774891776946035970E0,
                 6.91522889068984211695E0,
                 3.93881025292474443415E0,
                 1.33303460815807542389E0,
                 2.01485389549179081538E-1,
                 1.23716634817820021358E-2,
                 3.01581553508235416007E-4,
                 2.65806974686737550832E-6,
                 6.23974539184983293730E-9], dtype=dtype)
  q2 = np.array([1.0,
                 6.02427039364742014255E0,
                 3.67983563856160859403E0,
                 1.37702099489081330271E0,
                 2.16236993594496635890E-1,
                 1.34204006088543189037E-2,
                 3.28014464682127739104E-4,
                 2.89247864745380683936E-6,
                 6.79019408009981274425E-9], dtype=dtype)

  maybe_complement_p = jnp.where(p > dtype(-np.expm1(-2.)), dtype(1.) - p, p)
  # Write in an arbitrary value in place of 0 for p since 0 will cause NaNs
  # later on. The result from the computation when p == 0 is not used so any
  # number that doesn't result in NaNs is fine.
  sanitized_mcp = jnp.where(
      maybe_complement_p == dtype(0.),
      jnp.full(shape, dtype(0.5)),
      maybe_complement_p)

  # Compute x for p > exp(-2): x/sqrt(2pi) = w + w**3 P0(w**2)/Q0(w**2).
  w = sanitized_mcp - dtype(0.5)
  ww = lax.square(w)
  x_for_big_p = w + w * ww * (jnp.polyval(p0, ww) / jnp.polyval(q0, ww))
  x_for_big_p *= -dtype(np.sqrt(2. * np.pi))

  # Compute x for p <= exp(-2): x = z - log(z)/z - (1/z) P(1/z) / Q(1/z),
  # where z = sqrt(-2. * log(p)), and P/Q are chosen between two different
  # arrays based on whether p < exp(-32).
  z = lax.sqrt(dtype(-2.) * lax.log(sanitized_mcp))
  first_term = z - lax.log(z) / z
  second_term_small_p = jnp.polyval(p2, 1 / z) / jnp.polyval(q2, 1 / z) / z
  second_term_otherwise = jnp.polyval(p1, 1 / z) / jnp.polyval(q1, 1 / z) / z
  x_for_small_p = first_term - second_term_small_p
  x_otherwise = first_term - second_term_otherwise

  x = jnp.where(sanitized_mcp > dtype(np.exp(-2.)),
                x_for_big_p,
                jnp.where(z >= dtype(8.0), x_for_small_p, x_otherwise))

  x = jnp.where(p > dtype(1. - np.exp(-2.)), x, -x)
  with config.debug_infs(False):
    infinity = jnp.full(shape, dtype(np.inf))
    x = jnp.where(
        p == dtype(0.0), -infinity, jnp.where(p == dtype(1.0), infinity, x))
  if not isinstance(x, core.Tracer):
    try:
      dispatch.check_special("ndtri", [x])
    except api_util.InternalFloatingPointError as e:
      raise FloatingPointError(
          f"invalid value ({e.ty}) encountered in ndtri.") from None
  return x

