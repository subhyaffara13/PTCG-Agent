
def _array_global_result_handler(global_aval, out_sharding, committed):
  if global_aval.dtype == dtypes.float0:
    def handler(xs):
      return literals.TypedNdArray(np.zeros(global_aval.shape, dtypes.float0),
                                   aval=global_aval)
    phys_aval = core.physical_aval(global_aval)
    return xc.array_result_handler(phys_aval, out_sharding, committed=committed,
                                   _skip_checks=True).wrap(handler)
  if dtypes.issubdtype(global_aval.dtype, dtypes.extended):
    return global_aval.dtype._rules.global_sharded_result_handler(
        global_aval, out_sharding, committed)
  return xc.array_result_handler(
      global_aval, out_sharding, committed=committed, _skip_checks=True
  )

