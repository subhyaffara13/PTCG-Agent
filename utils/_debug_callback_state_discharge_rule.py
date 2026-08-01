
def _debug_callback_state_discharge_rule(
    in_avals, out_avals, *args, effect, partitioned, callback, **params
):
  del in_avals, out_avals  # Unused.
  out = debug_callback_p.bind(
      *args, effect=effect, partitioned=partitioned, callback=callback, **params
  )
  return args, out

