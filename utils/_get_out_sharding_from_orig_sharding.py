
def _get_out_sharding_from_orig_sharding(
    out_shardings, out_avals, orig_in_s, orig_aval):
  out: list[JSharding] = []
  orig_handler = _orig_out_sharding_handlers[type(orig_in_s)]
  for o, out_aval in safe_zip(out_shardings, out_avals):
    if (isinstance(o, sharding_impls.GSPMDSharding) and
        out_aval is not core.abstract_token):
      # TODO(yashkatariya): Remove this condition and ask users to drop into
      # explicit mode.
      if (orig_aval is not None and out_aval is not None
          and out_aval.ndim == orig_aval.ndim
          and isinstance(orig_in_s, NamedSharding)
          and out_aval.sharding.mesh == orig_in_s.mesh.abstract_mesh
          and o.is_equivalent_to(orig_in_s, orig_aval.ndim)):
        out.append(orig_in_s)
      else:
        try:
          out.append(orig_handler(o, out_aval, orig_in_s))
        except IndivisibleError:
          raise
        except:
          out.append(o)
    else:
      out.append(o)
  return out

