
def _device_put_impl(
    x, *, device: Device | Sharding | Format | None,
    src: Device | Sharding | Format | None, copy: ArrayCopySemantics, aval):
  if aval is None:
    try:
      if isinstance(x, core.Tracer):
        raise TypeError(f"Argument '{x}' of type '{type(x)}' is not a valid JAX type")
      aval = core.typeof(x)
      aval = update_dp_aval(aval, device)
    except TypeError as err:
      raise TypeError(
          f"Argument '{x}' of type {type(x)} is not a valid JAX type") from err

  if isinstance(device, core.MemorySpace):
    return apply_primitive(device_put_p, x, devices=(device,), srcs=(src,),
                           copy_semantics=(copy,))[0]

  if isinstance(device, Format):
    l = device
    dll = l.layout
    x_dll = x.format.layout if hasattr(x, 'format') else None
    if dll is None and l.sharding is None:
      return _device_put_sharding_impl(x, aval, l.sharding, copy)
    if (not isinstance(l.sharding, Sharding) or
        not isinstance(dll, (Layout, type(None)))):
      raise ValueError(
          "sharding and layout in `Layout` instance should be"
          f" concrete. Got layout: {l} for input {aval.str_short()}")
    if (getattr(x, 'format', None) == l and getattr(x, '_committed', False) and
        copy == ArrayCopySemantics.REUSE_INPUT):
      return x
    if x_dll is None and dll is None:
      return _device_put_sharding_impl(x, aval, l.sharding, copy)
    return api.jit(
        _device_put_reshard,
        out_shardings=l,
        donate_argnums=(0 if copy == ArrayCopySemantics.DONATE_INPUT else None),
    )(x)

  return _device_put_sharding_impl(x, aval, device, copy)

