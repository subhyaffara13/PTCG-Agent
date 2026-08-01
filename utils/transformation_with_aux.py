
def transformation_with_aux(gen, fun: WrappedFun, *gen_static_args) -> WrappedFun:
  def gen2(f, store, *args, **kwargs):
    gen_inst = gen(*args, **kwargs)
    args_, kwargs_ = next(gen_inst)
    ans, aux = gen_inst.send(f(*args_, **kwargs_))
    store.store(aux)
    return ans
  return transformation_with_aux2(gen2, fun, *gen_static_args)()

