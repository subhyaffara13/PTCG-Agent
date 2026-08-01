
def _pretty_slice(s: slice) -> str:
  start = s.start if s.start is not None else ''
  stop = s.stop if s.stop is not None else ''
  step = f':{s.step}' if s.step is not None else ''
  return f'{start}:{stop}{step}'

