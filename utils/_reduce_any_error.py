
def _reduce_any_error(error: Error):
  out_error = init_error
  for error_effect in error._pred.keys():
    errs, codes, payloads = (error._pred[error_effect],
                             error._code[error_effect],
                             error._payload[error_effect])
    reduced_idx = jnp.argsort(errs)[-1]
    pred, code, payload = tree_map(lambda x, idx=reduced_idx: x[idx],
                                   (errs, codes, payloads))
    out_error = out_error._update(error_effect, pred, code, {}, payload)

  out_error = out_error._replace(_metadata=error._metadata)
  return out_error

