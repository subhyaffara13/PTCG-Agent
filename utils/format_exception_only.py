
def format_exception_only(e: BaseException) -> str:
  return ''.join(traceback.format_exception_only(type(e), e)).strip()

