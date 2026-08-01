
def _maybe_canonicalize_explicit_dtype(dtype: DType, fun_name: str) -> DType:
  "Canonicalizes explicitly requested dtypes, per explicit_x64_dtypes."
  allow = config.explicit_x64_dtypes.value
  if allow == config.ExplicitX64Mode.ALLOW or config.enable_x64.value:
    return dtype
  canonical_dtype = canonicalize_dtype(dtype)
  if canonical_dtype == dtype:
    return dtype
  fun_name = f" requested in {fun_name}" if fun_name else ""
  if allow == config.ExplicitX64Mode.ERROR:
    msg = ("Explicitly requested dtype {}{} is not available. To enable more "
           "dtypes, set the jax_enable_x64 or allow_explicit_x64_dtypes "
           "configuration options."
          "See https://github.com/jax-ml/jax#current-gotchas for more.")
    msg = msg.format(dtype, fun_name, canonical_dtype.name)
    raise ValueError(msg)
  else:  # WARN
    msg = ("Explicitly requested dtype {}{} is not available, "
          "and will be truncated to dtype {}. To enable more dtypes, set the "
          "jax_enable_x64 configuration option or the JAX_ENABLE_X64 shell "
          "environment variable. "
          "See https://github.com/jax-ml/jax#current-gotchas for more.")
    msg = msg.format(dtype, fun_name, canonical_dtype.name)
    warnings.warn(msg, stacklevel=4)
    return canonical_dtype

