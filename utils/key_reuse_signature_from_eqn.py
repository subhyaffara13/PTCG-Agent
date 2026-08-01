
def key_reuse_signature_from_eqn(eqn: core.JaxprEqn) -> KeyReuseSignature:
  if eqn.primitive in key_reuse_signatures:
    sig = key_reuse_signatures[eqn.primitive]
    if isinstance(sig, KeyReuseSignature):
      return sig
    elif isinstance(sig, DynamicKeyReuseSignature):
      return sig.signature(eqn)
    else:
      raise TypeError(
        f"Unrecognized key reuse signature of type {type(sig)}: {sig}")
  else:
    return unknown_signature(eqn)

