
def make_scalar_prefetch_handler(*args):
  def scalar_prefetch_getter(*sp_inputs):
    result = sp_inputs
    for i in args:
      result = result[i]
    return result

  return scalar_prefetch_getter

