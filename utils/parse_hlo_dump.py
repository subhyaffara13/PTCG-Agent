
def parse_hlo_dump(text: str) -> sourcemap.SourceMap:
  lines = text.split("\n")
  if "FileNames" in text:
    return _parse_hlo_new_format(lines)
  return _parse_hlo_old_format(lines)

