
def const_args_layouts(
    const_args: Sequence[ArrayLike],
    avals: Sequence[core.AbstractValue],
    shardings: Sequence[PjitSharding]
    ) -> Sequence[Layout | AutoLayoutSingleton | None]:
  const_args_types = map(convert_to_metaty, const_args)
  return _resolve_in_layouts(
      const_args_types, (None,) * len(const_args), shardings, avals)

