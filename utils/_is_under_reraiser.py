
def _is_under_reraiser(e: BaseException) -> bool:
  if e.__traceback__ is None:
    return False
  tb = traceback.extract_stack(e.__traceback__.tb_frame)
  return any(_is_reraiser_frame(f) for f in tb[:-1])

