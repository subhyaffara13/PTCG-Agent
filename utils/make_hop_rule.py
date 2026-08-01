
def make_hop_rule(primitive, *keys):
  """Makes a rule for higher-order ops by recursively applying the jaxpr pass.

  Args:
    primitive: A JAX primitive.
    keys: The names of parameters which correspond to Jaxprs that need
      to be recursed over.

  Returns:
    A primitive rule for the edtype Jaxpr pass. This should be registered
    using `register_edtype_rule`.
  """
  def _resolve_jaxpr(interpreter,
                     value: jax_core.Jaxpr | jax_core.ClosedJaxpr,
                     mapped_idx=None):
    extra_args = ()
    if isinstance(value, jax_core.Jaxpr):
      if len(value.constvars) > 0:
        raise ValueError(f"Cannot physicalize a jaxpr with constvars: {value}")
      physical_jaxpr, physical_consts = interpreter(value, ())
      if physical_consts:
        if mapped_idx is not None:
          new_jaxpr = pad_jaxpr_constvars(physical_jaxpr,
                                          mapped_idx,
                                          physical_consts)
          extra_args = tuple(physical_consts)
        else:
          new_jaxpr = pe.convert_constvars_jaxpr(physical_jaxpr)
          extra_args = tuple(physical_consts)
      else:
        new_jaxpr = physical_jaxpr
    elif isinstance(value, jax_core.ClosedJaxpr):
      jaxpr, new_consts = interpreter(value.jaxpr, value.consts)
      new_jaxpr = jax_core.ClosedJaxpr(jaxpr, new_consts)
    else:
      raise ValueError(f"Parameter of type {type(value)} is not a Jaxpr.")
    return new_jaxpr, extra_args

  def rule(interpreter, *args, **params):
    new_params = {}
    for key in keys:
      value = params[key]
      if isinstance(value, jax_core.Jaxpr) or isinstance(
          value, jax_core.ClosedJaxpr):
        new_jaxpr, extra_args = _resolve_jaxpr(interpreter, value)
        new_params[key] = new_jaxpr
        args = extra_args + args
      elif isinstance(value, tuple) or isinstance(value, list):
        mapped_jaxprs, mapped_args = zip(*map(
          lambda x, i: _resolve_jaxpr(interpreter, x, mapped_idx=i), value, range(len(value))))
        all_new_args = tuple(new_arg for _args in mapped_args for new_arg in _args)
        new_params[key] = tuple(mapped_jaxprs)
        args = all_new_args + args
      else:
        raise ValueError(f"Parameter {key} is not a Jaxpr or sequence of Jaxprs: {value}")
    params.update(new_params)
    return primitive.bind(*args, **params)
  return rule

