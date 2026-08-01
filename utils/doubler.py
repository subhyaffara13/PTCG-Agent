
def doubler(f):
  def inner(*args, **kwds):
    fx = f(*args, **kwds)
    return 2*fx
  return inner

