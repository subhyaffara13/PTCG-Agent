
def choose_device_or_out_sharding(device: xc.Device | Sharding | None,
                                  out_sharding: NamedSharding | P | None,
                                  name: str) -> Sharding | NamedSharding | None:
  if device is not None and out_sharding is not None:
    raise ValueError(
        f"Only one of `device` or `out_sharding` can be set. Got {device=} and"
        f" {out_sharding=}")
  if device is not None and out_sharding is None:
    return canonicalize_device_to_sharding(device)
  if device is None and out_sharding is not None:
    return canonicalize_sharding(out_sharding, name)
  return None

