
def key_reuse_signature_from_primitive(prim, *args, **params):
  if prim == pjit.jit_p:
    return jaxpr_type_signature(params['jaxpr'].jaxpr)
  if prim not in key_reuse_signatures:
    # TODO(jakevdp) should we generate an unknown signature here?
    raise RuntimeError(f"Internal: no key reuse rule for primitive {prim}")
  sig = key_reuse_signatures[prim]
  if isinstance(sig, KeyReuseSignature):
    return sig
  elif isinstance(sig, DynamicKeyReuseSignature):
    jaxpr = jax.make_jaxpr(partial(prim.bind, **params))(*args).jaxpr
    return jaxpr_type_signature(jaxpr)
  else:
    raise TypeError(
      f"Unrecognized key reuse signature of type {type(sig)}: {sig}")

