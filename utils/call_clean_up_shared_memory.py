
def call_clean_up_shared_memory(token):
  return callback.io_callback(
      _clean_up_shared_memory, TOKEN_SHAPE_DTYPE, token
  )

