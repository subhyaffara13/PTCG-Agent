
def _ignore_known_hidden_frame(f: types.FrameType) -> bool:
  return 'importlib._bootstrap' in f.f_code.co_filename

