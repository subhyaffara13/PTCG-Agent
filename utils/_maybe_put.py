
def _maybe_put(x):
  if isinstance(x, np.ndarray):
    aval = core.shaped_abstractify(x)
    s = sharding.make_single_device_sharding(
        xb.local_devices(backend='cpu')[0])
    result_handler = pxla.global_aval_to_result_handler(aval, s, False)
    return result_handler(
        pxla.shard_args(
            [s], [None], [dispatch.ArrayCopySemantics.REUSE_INPUT], [x]
        )
    )
  else:
    return x

