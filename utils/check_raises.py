
def check_raises(thunk, err_type, msg):
  try:
    thunk()
    assert False
  except err_type as e:
    assert str(e).startswith(msg), f"\n{e}\n\n{msg}\n"

