
def resolve_prng_impl(
    impl_spec: PRNGSpecDesc | KeyDTypeLike | None,
) -> PRNGImpl:
  if impl_spec is None:
    return default_prng_impl()
  if type(impl_spec) is PRNGImpl:
    # TODO(frostig,vanderplas): remove this case once we remove
    # default_prng_impl (and thus PRNGImpl) from the public API and
    # PRNGImpl from jex. We won't need to handle these then, and we
    # can remove them from the input type annotation above as well.
    return impl_spec
  if type(impl_spec) is PRNGSpec:
    return impl_spec._impl
  if isinstance(impl_spec, prng.KeyTy):
    return impl_spec._impl
  if type(impl_spec) is str:
    if impl_spec in prng.prngs:
      return prng.prngs[impl_spec]

    keys_fmt = ', '.join(f'"{s}"' for s in prng.prngs.keys())
    raise ValueError(f'unrecognized PRNG implementation "{impl_spec}". '
                     f'Did you mean one of: {keys_fmt}?')

  t = type(impl_spec)
  raise TypeError(f"unrecognized type {t} for specifying PRNG implementation.")

