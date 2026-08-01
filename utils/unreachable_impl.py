
def unreachable_impl(*_, out_avals, exc_type, message):
  del out_avals
  raise exc_type(message)

