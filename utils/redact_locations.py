import re

def redact_locations(err_msg: str) -> str:
  """Removes location strings from an error message."""
  for mat in re.finditer(LOCATION_PATTERN, err_msg):
    start, end = mat.span('location')
    # Remove the entire line containing the location.
    line_start = err_msg.rfind('\n', 0, end)
    line_start = line_start if line_start >= 0 else start
    line_end = err_msg.find('\n', start)
    line_end = line_end if line_end >= 0 else end
    return err_msg[:line_start] + err_msg[line_end+1:]
  return err_msg

