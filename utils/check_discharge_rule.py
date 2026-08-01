
def check_discharge_rule(error, enabled_errors, *args, err_tree, debug):
  del debug
  new_error = tree_unflatten(err_tree, args)
  # Split up new_error into error to be functionalized if it's included in
  # enabled_errors (=discharged_error) and an error to be defunctionalized if
  # it's not included (=recharged_error)
  discharged_error = error
  recharged_error = init_error
  for error_effect in new_error._pred.keys():
    pred = new_error._pred[error_effect]
    code = new_error._code[error_effect]
    payload = new_error._payload[error_effect]
    if error_effect.error_type in enabled_errors:
      discharged_error = update_error(discharged_error, pred, code, {}, payload,
                                      error_effect)
    else:
      recharged_error = update_error(recharged_error, pred, code, {}, payload,
                                     error_effect)

  discharged_error = discharged_error._replace(
      _metadata={**new_error._metadata, **discharged_error._metadata})
  recharged_error = recharged_error._replace(_metadata=new_error._metadata)
  # TODO(lenamartens): we actually need to recharge, but this would be a
  # breaking API change so leaving for a follow-up.
  # check_error(recharged_error)
  return discharged_error, []

