
def _call_exported_impl(*args, exported: Exported):
  return dispatch.apply_primitive(call_exported_p, *args, exported=exported)

