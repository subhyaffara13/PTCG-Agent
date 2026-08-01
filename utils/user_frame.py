
def user_frame(traceback: Traceback | None) -> Frame | None:
  return next(user_frames(traceback), None)

