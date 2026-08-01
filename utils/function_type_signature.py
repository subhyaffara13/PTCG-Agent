
def function_type_signature(fun: Callable[..., Any], *args: Any) -> KeyReuseSignature:
  args_flat, in_tree = tree_util.tree_flatten(args)
  in_avals_flat = [core.typeof(arg) for arg in args_flat]
  wrapped_fun, _ = api_util.flatten_fun_nokwargs(
      lu.wrap_init(fun,
                   debug_info=api_util.debug_info("key_reuse", fun, args, {})),
      in_tree)
  jaxpr, _, _ = pe.trace_to_jaxpr_dynamic(wrapped_fun, in_avals_flat)
  return jaxpr_type_signature(jaxpr)

