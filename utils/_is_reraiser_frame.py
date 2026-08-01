
def _is_reraiser_frame(f: traceback.FrameSummary | types.FrameType) -> bool:
  if isinstance(f, traceback.FrameSummary):
    filename, name = f.filename, f.name
  else:
    filename, name = f.f_code.co_filename, f.f_code.co_name
  return filename == __file__ and name == 'reraise_with_filtered_traceback'

