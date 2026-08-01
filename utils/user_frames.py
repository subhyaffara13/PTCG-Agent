
def user_frames(traceback: Traceback | None) -> Iterator[Frame]:
  """Iterator over the user's frames, filtering jax-internal frames."""
  # Guess the user's frame is the innermost frame not in the jax source tree or
  # Python stdlib. We don't use traceback_util.path_starts_with because that
  # incurs filesystem access, which may be slow; we call this function when
  # e.g. adding source provenance annotations to XLA lowerings, so we don't
  # want to incur the cost. We consider files that end with _test.py as user
  # frames, to allow testing this mechanism from tests.
  code, lasti = traceback.raw_frames() if traceback else ([], [])
  return (raw_frame_to_frame(code[i], lasti[i]) for i in range(len(code))
          if is_user_filename(code[i].co_filename))

