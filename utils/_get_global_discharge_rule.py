
def _get_global_discharge_rule(in_avals, out_avals, *, what):
  del in_avals, out_avals, what
  raise NotImplementedError(
      "get_global discharge is not supported in interpret mode."
  )

