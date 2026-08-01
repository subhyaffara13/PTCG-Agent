
def to_linen(
    nnx_class: tp.Callable[..., Module],
    *args,
    metadata_fn: (
        tp.Callable[[variablelib.Variable], tp.Any] | None
    ) = bv.to_linen_var,
    name: str | None = None,
    skip_rng: bool = False,
    abstract_init: bool = True,
    **kwargs,
):
  """Shortcut of `nnx.bridge.ToLinen` if user is not changing any of its default fields."""
  return ToLinen(
      nnx_class,
      args=args,
      kwargs=FrozenDict(kwargs),
      metadata_fn=metadata_fn,
      skip_rng=skip_rng,
      name=name,
  )

