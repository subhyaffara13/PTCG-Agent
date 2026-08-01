
def _async_wrapped(func):
  @functools.wraps(func)
  async def wrapper(*args, **kwargs):
    return await func(*args, **kwargs)
  return wrapper

