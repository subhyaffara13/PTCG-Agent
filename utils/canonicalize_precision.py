
def canonicalize_precision(precision: PrecisionLike) -> CanonicalPrecision:
  """Turns an API precision specification into a pair of enumeration values.

  The API can take the precision as a string, or int, and either as a single
  value to apply to both operands, or as a sequence of two values.
  """
  if precision is None:
    if config.default_matmul_precision.value is None:
      return None
    try:
      return canonicalize_precision(config.default_matmul_precision.value)
    except ValueError:
      raise ValueError(
          "jax_default_matmul_precision flag must be set to None, a value in "
          f"{list(_precision_strings)}, or the name of a lax.DotAlgorithmPreset, "
          f"but got {config.default_matmul_precision.value}"
      ) from None
  elif isinstance(precision, str):
    if precision in _precision_strings:
      return Precision(precision), Precision(precision)
    else:
      try:
        return DotAlgorithmPreset[precision]
      except KeyError:
        pass
  elif isinstance(precision, Precision):
    return precision, precision
  elif isinstance(precision, (DotAlgorithm, DotAlgorithmPreset)):
    return precision
  elif (isinstance(precision, (list, tuple)) and len(precision) == 2 and
        all(isinstance(p, Precision) for p in precision)):
    return type_cast(tuple[Precision, Precision], precision)
  elif (isinstance(precision, (list, tuple)) and len(precision) == 2 and
        all(isinstance(s, str) for s in precision)):
    s1, s2 = type_cast(tuple[str, str], precision)
    p1 = type_cast(tuple[Precision, Precision], canonicalize_precision(s1))[0]
    p2 = type_cast(tuple[Precision, Precision], canonicalize_precision(s2))[0]
    return (p1, p2)
  raise ValueError(
      "Precision argument must be one of:\n"
      "- None,\n"
      f"- a string in {list(_precision_strings)},\n"
      "- a lax.Precision value,\n"
      "- a tuple of two lax.Precision values or strings,\n"
      "- a lax.DotAlgorithmPreset or the name of one of these presets, or\n"
      "- a lax.DotAlgorithm value;\n"
      f"but got {precision}.")

