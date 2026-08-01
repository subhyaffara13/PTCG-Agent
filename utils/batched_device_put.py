
def batched_device_put(aval: core.ShapedArray,
                       sharding: JSharding, xs: Sequence[Any],
                       devices: Sequence[xc.Device], committed: bool = True,
                       enable_x64: bool | None = None):
  util.test_event("batched_device_put_start")
  try:
    bufs = [x for x, d in safe_zip(xs, devices)
            if (isinstance(x, array.ArrayImpl) and x.sharding.num_devices == 1
                and x.devices() == {d})]
    if len(bufs) == len(xs) > 0:
      return array.ArrayImpl(
          aval, sharding, bufs, committed=committed, _skip_checks=True)
    return xc.batched_device_put(aval, sharding, xs, list(devices), committed,
                                 enable_x64=enable_x64)
  finally:
    util.test_event("batched_device_put_end")

