
def transformation(gen, fun: WrappedFun, *gen_static_args) -> WrappedFun:
  def gen2(f, *args, **kwargs):
    gen_inst = gen(*args, **kwargs)
    args_, kwargs_ = next(gen_inst)
    return gen_inst.send(f(*args_, **kwargs_))
  return transformation2(gen2, fun, *gen_static_args)()

