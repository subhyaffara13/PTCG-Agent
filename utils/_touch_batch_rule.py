
def _touch_batch_rule(args, dims):
  del dims
  touch_p.bind(*args)
  return [], ()

