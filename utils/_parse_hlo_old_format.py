
def _parse_hlo_old_format(lines: list[str]) -> sourcemap.SourceMap:
  mappings = sourcemap.MappingsGenerator()
  used_source_files = []
  for line in lines:
    mappings.new_group()
    match = METADATA_REGEX.search(line)
    if match:
      match_dict = match.groupdict()
      _ = match_dict["scope"]  # Unused
      src_file = match_dict["src_file"]
      src_line = int(match_dict["src_line"])
      if src_file not in used_source_files:
        used_source_files.append(src_file)
      src_file_idx = used_source_files.index(src_file)
      src_line -= 1  # Segments are zero-indexed
      first_col = line.index(line.strip()[0])
      mappings.new_segment(first_col, src_file_idx, src_line, 0)
  mappings.new_group()

  return sourcemap.SourceMap(
      version=3,
      sources=used_source_files,
      sources_content=[],
      mappings=mappings.mappings(),
      names=[],
  )

