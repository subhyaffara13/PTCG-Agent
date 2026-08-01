
def call_assert_no_barriers_allocated(token):
  return callback.io_callback(
      _assert_no_barriers_allocated, TOKEN_SHAPE_DTYPE, token
  )

