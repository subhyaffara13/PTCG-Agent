
def dynamic_key_reuse_signature(f: Callable[[core.JaxprEqn], KeyReuseSignature]) -> DynamicKeyReuseSignature:
  return DynamicKeyReuseSignature(f)

