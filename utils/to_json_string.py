
def to_json_string(duration: Duration) -> str:
  """Converts Duration to string format.

  Returns:
    A string converted from self. The string format will contains
    3, 6, or 9 fractional digits depending on the precision required to
    represent the exact Duration value. For example: "1s", "1.010s",
    "1.000000100s", "-3.100s"
  """
  return duration.ToJsonString()


def to_json_string(ts: Timestamp) -> str:
  """Converts Timestamp to RFC 3339 date string format.

  Returns:
    A string converted from timestamp. The string is always Z-normalized
    and uses 3, 6 or 9 fractional digits as required to represent the
    exact time. Example of the return format: '1972-01-01T10:00:20.021Z'
  """
  return ts.ToJsonString()

