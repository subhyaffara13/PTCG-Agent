
def _ignore_axis_index_groups(fn):
  """Wrapper that forces axis_index_groups to be None.

  This is to avoid problems within fake_pmap where parallel operations are
  performed with vmap, rather than pmap. Parallel operations where
  `axis_index_groups` is not `None` are not currently supported under vmap.

  Args:
    fn: the function to wrap

  Returns:
    a wrapped function that forces any keyword argument named
      `axis_index_groups` to be None
  """
  @functools.wraps(fn)
  def _fake(*args, axis_index_groups=None, **kwargs):
    del axis_index_groups
    return fn(*args, axis_index_groups=None, **kwargs)
  return _fake

