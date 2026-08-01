
def call_impl_with_key_reuse_checks(prim: core.Primitive, raw_impl: Callable[..., Any], *args, **kwargs) -> Any:
  if prim not in key_reuse_signatures:
    # TODO(jakevdp): should we use an unknown signature here?
    return raw_impl(*args, **kwargs)
  signature = key_reuse_signature_from_primitive(prim, *args, **kwargs)
  funcname = "jit-compiled function" if prim == pjit.jit_p else str(prim)
  consts = kwargs['jaxpr'].consts if prim == pjit.jit_p else []
  signature.check_signature(*args, *consts, funcname=funcname)
  result = raw_impl(*args, **kwargs)
  signature.update_consumption([*args, *consts], result if prim.multiple_results else [result])
  return result

