
def _pp_device_id(device_id, context):
  if device_id is None:
    return pp.text("None")
  elif isinstance(device_id, dict):
    items = []
    for k, v in device_id.items():
      item = pp.concat([pp.text(f"{k}: "), _pp_device_id(v, context)])
      items.append(item)
    return pp.concat(
        [pp.text("{"), pp.join(pp.text(", "), items), pp.text("}")]
    )
  elif isinstance(device_id, tuple):
    items = [_pp_device_id(v, context) for v in device_id]
    return pp.concat(
        [pp.text("("), pp.join(pp.text(", "), items), pp.text(")")]
    )
  elif isinstance(device_id, list):
    items = [_pp_device_id(v, context) for v in device_id]
    return pp.concat(
        [pp.text("["), pp.join(pp.text(", "), items), pp.text("]")]
    )
  else:
    return jax_core.pp_var(device_id, context)

