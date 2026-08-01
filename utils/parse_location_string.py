
def parse_location_string(location_string: str) -> tuple[str, list[RawFrame]]:
  """Parses a serialized MLIR location.

  Locations strings have the format:
  `loc("location_name"(<callsite>))`

  Where <callsite> is a nested callsite string representing the entire
  call stack:
  `callsite("fn_name"("filename":lineno:colno) at callsite(...))`

  Args:
    location_string: A string serialization of an MLIR location.

  Returns:
    A tuple (name, frames) where name is the name of the location and frames
    is a list of RawFrame objects representing the Python call stack associated
    with the location.
  """
  frame_str = ''
  loc_name = None
  matches = list(re.finditer(LOCATION_PATTERN, location_string))
  if len(matches) > 1:
    raise ValueError(
        'More than one location found in string: ', location_string)
  for mat in matches:
    loc_name = mat.group('eqn_str')[1:-1]
    frame_str = mat.group('frames')[1:-1]
  if loc_name is None:
    raise ValueError(f'Could not find location in string {location_string}')
  frames: list[RawFrame] = []
  for mat in re.finditer(FRAME_PATTERN, frame_str):
    frames.append(
        RawFrame(
            mat.group('fun_name')[1:-1],
            mat.group('filename')[1:-1],
            int(mat.group('lineno')),
            int(mat.group('colno')),
        )
    )
  return loc_name, frames

