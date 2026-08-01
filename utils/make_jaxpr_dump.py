
def make_jaxpr_dump(jaxpr: core.Jaxpr, **_) -> common.SourceMapDump:
  pprint_mappings: list[list[tuple[int, int, Any]]] = []
  pprint_str = jaxpr.pretty_print(source_map=pprint_mappings)
  used_source_files = []
  mappings = sourcemap.MappingsGenerator()
  for pprint_map_line in pprint_mappings:
    mappings.new_group()
    for pprint_segment in pprint_map_line:
      start_col, end_col, tb = pprint_segment
      del end_col
      frame = source_info_util.user_frame(tb)
      if frame is None:
        continue
      file_name = canonicalize_filename(frame.file_name)
      if file_name not in used_source_files:
        used_source_files.append(file_name)
      file_idx = used_source_files.index(file_name)
      src_line = frame.start_line - 1  # Zero-indexed
      src_col = frame.start_column
      # A segment is a tuple of the form:
      # (generated_col, src_file_idx, src_line, src_col)
      mappings.new_segment(start_col, file_idx, src_line, src_col)
  mappings.new_group()
  source_map = sourcemap.SourceMap(
      version=3,
      sources=used_source_files,
      sources_content=[],
      mappings=mappings.mappings(),
      names=[],
  )
  return common.SourceMapDump(
      source_map=source_map,
      generated_code=pprint_str,
      pass_name='jaxpr',
  )

