
def update_error(error, pred, code, metadata, payload, effect_type):
  err_of_type = error._pred.get(effect_type, False)
  out_err = err_of_type | pred
  out_code = lax.select(err_of_type, error._code.get(effect_type, -1), code)
  cur_payload = error._payload.get(effect_type, None)
  if cur_payload is not None:
    out_payload = tree_map(functools.partial(lax.select, err_of_type), cur_payload, payload)
  else:
    out_payload = payload
  return error._update(effect_type, out_err, out_code, metadata, out_payload)

