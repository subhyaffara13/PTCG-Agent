
def include_frame(f: types.FrameType) -> bool:
  return include_filename(f.f_code.co_filename)

