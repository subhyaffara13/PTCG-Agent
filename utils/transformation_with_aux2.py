
def transformation_with_aux2(
    gen, fun: WrappedFun, *gen_static_args, use_eq_store: bool = False,
    unk_names: bool = False) -> tuple[WrappedFun, Callable[[], Any]]:
  """Adds one more transformation with auxiliary output to a WrappedFun."""
  out_store = Store() if not use_eq_store else EqualStore()
  out_thunk = lambda: out_store.val
  fun = fun.wrap(gen, gen_static_args, out_store)
  fun = fun.with_unknown_names() if unk_names else fun
  return fun, out_thunk

