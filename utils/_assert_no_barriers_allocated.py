
def _assert_no_barriers_allocated(token):
  _get_shared_memory().assert_no_barriers_allocated()
  return token

