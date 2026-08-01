
def traceback_from_raw_frames(frames: list[RawFrame]) -> types.TracebackType:
  """Constructs a traceback from a list of RawFrame objects."""
  xla_frames = [
    xla_client.Frame(frame.filename, frame.func_name, -1, frame.lineno)
    for frame in frames
  ]
  return xla_client.Traceback.traceback_from_frames(xla_frames)

