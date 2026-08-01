
def get_races() -> RaceDetectionState:
  assert _races is not None
  return _races


def get_races() -> gpu_callbacks.RaceDetectionState:
  return gpu_callbacks.get_races()

