
def _terminal_link(uri: str, text: str) -> str:
  """Returns a clickable link on the terminal."""
  parameters = ''
  # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
  return f'\033]8;{parameters};{uri}\033\\{text}\033]8;;\033\\'

