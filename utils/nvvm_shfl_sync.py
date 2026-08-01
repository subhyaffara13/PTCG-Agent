
def nvvm_shfl_sync(ty, *args):
  first_param, *_ = inspect.signature(nvvm.shfl_sync).parameters.keys()
  if first_param != "thread_mask":
    return nvvm.shfl_sync(ty, *args)
  else:
    return nvvm.shfl_sync(*args, results=[ty])

