
def const_args_shardings(const_args: Sequence[Array | np.ndarray]) -> Sequence[PjitSharding]:
  const_args_types = map(convert_to_metaty, const_args)
  return _resolve_in_shardings(
      const_args_types, (sharding_impls.UNSPECIFIED,) * len(const_args))

