
def custom_hook() -> str:
  """Custom hook for any addition to the cache key.

  The custom hook will be called every time get() is called and can be
  defined to return a string that will be hashed into the cache key.
  """
  return ""

