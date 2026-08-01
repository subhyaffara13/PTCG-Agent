
def _least_upper_bound(jax_numpy_dtype_promotion: config.NumpyDtypePromotion,
                       x64: bool, *nodes: JAXType) -> JAXType:
  """Compute the least upper bound of a set of nodes.

  Args:
    nodes: sequence of entries from _jax_types + _weak_types
  Returns:
    the _jax_type representing the least upper bound of the input nodes
      on the promotion lattice.
  """
  # This function computes the least upper bound of a set of nodes N within a partially
  # ordered set defined by the lattice generated above.
  # Given a partially ordered set S, let the set of upper bounds of n ∈ S be
  #   UB(n) ≡ {m ∈ S | n ≤ m}
  # Further, for a set of nodes N ⊆ S, let the set of common upper bounds be given by
  #   CUB(N) ≡ {a ∈ S | ∀ b ∈ N: a ∈ UB(b)}
  # Then the least upper bound of N is defined as
  #   LUB(N) ≡ {c ∈ CUB(N) | ∀ d ∈ CUB(N), c ≤ d}
  # The definition of an upper bound implies that c ≤ d if and only if d ∈ UB(c),
  # so the LUB can be expressed:
  #   LUB(N) = {c ∈ CUB(N) | ∀ d ∈ CUB(N): d ∈ UB(c)}
  # or, equivalently:
  #   LUB(N) = {c ∈ CUB(N) | CUB(N) ⊆ UB(c)}
  # By definition, LUB(N) has a cardinality of 1 for a partially ordered set.
  # Note a potential algorithmic shortcut: from the definition of CUB(N), we have
  #   ∀ c ∈ N: CUB(N) ⊆ UB(c)
  # So if N ∩ CUB(N) is nonempty, if follows that LUB(N) = N ∩ CUB(N).
  N = set(nodes)
  if jax_numpy_dtype_promotion == config.NumpyDtypePromotion.STRICT:
    UB = _strict_lattice_ubs
  elif jax_numpy_dtype_promotion == config.NumpyDtypePromotion.STANDARD:
    if x64:
      UB = _standard_x64_lattice_ubs
    else:
      UB = _standard_x32_lattice_ubs
  else:
    raise ValueError(
      f"Unexpected value of jax_numpy_dtype_promotion={jax_numpy_dtype_promotion!r}")
  try:
    bounds = [UB[n] for n in N]
  except KeyError:
    dtype = next(n for n in N if n not in UB)
    raise ValueError(f"{dtype=} is not a valid dtype for JAX type promotion.")
  CUB = set.intersection(*bounds)
  LUB = (CUB & N) or {c for c in CUB if CUB.issubset(UB[c])}
  if len(LUB) == 1:
    return LUB.pop()
  elif len(LUB) == 0:
    if config.numpy_dtype_promotion.value == config.NumpyDtypePromotion.STRICT:
      msg = (
        f"Input dtypes {tuple(str(n) for n in nodes)} have no available implicit dtype "
        "promotion path when jax_numpy_dtype_promotion=strict. Try explicitly casting "
        "inputs to the desired output type, or set jax_numpy_dtype_promotion=standard.")
    elif any(n in _float8_dtypes for n in nodes):
      msg = (
        f"Input dtypes {tuple(str(n) for n in nodes)} have no available implicit dtype "
        "promotion path. To avoid unintended promotion, 8-bit floats do not support "
        "implicit promotion. If you'd like your inputs to be promoted to another type, "
        "you can do so explicitly using e.g. x.astype('float32')")
    elif any(n in _float6_dtypes for n in nodes):
      msg = (
        f"Input dtypes {tuple(str(n) for n in nodes)} have no available implicit dtype "
        "promotion path. To avoid unintended promotion, 6-bit floats do not support "
        "implicit promotion. If you'd like your inputs to be promoted to another type, "
        "you can do so explicitly using e.g. x.astype('float32')")
    elif any(n in _float4_dtypes for n in nodes):
      msg = (
        f"Input dtypes {tuple(str(n) for n in nodes)} have no available implicit dtype "
        "promotion path. To avoid unintended promotion, 4-bit floats do not support "
        "implicit promotion. If you'd like your inputs to be promoted to another type, "
        "you can do so explicitly using e.g. x.astype('float32')")
    elif any(n in _intn_dtypes for n in nodes):
      msg = (
          f'Input dtypes {tuple(str(n) for n in nodes)} have no available'
          ' implicit dtype promotion path. To avoid unintended promotion,'
          ' 1-bit, 2-bit and 4-bit integers do not support implicit promotion.'
          " If you'd like your inputs to be promoted to another type, you can"
          " do so explicitly using e.g. x.astype('int32')"
      )
    else:
      msg = (
        f"Input dtypes {tuple(str(n) for n in nodes)} have no available implicit dtype "
        "promotion path. Try explicitly casting inputs to the desired output type.")
    raise TypePromotionError(msg)
  else:
    # If we get here, it means the lattice is ill-formed.
    raise TypePromotionError(
      f"Internal Type Promotion error: {nodes} do not have a unique least upper bound "
      f"on the specified lattice; options are {LUB}. This is an unexpected error in "
      "JAX's internal logic; please report it to the JAX maintainers."
    )

