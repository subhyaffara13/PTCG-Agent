
def call_impl(f: lu.WrappedFun, *args, **params):
  del params  # params parameterize the call primitive, not the function
  return f.call_wrapped(*args)

