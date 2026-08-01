
def create_mlir_sourcemap(mlir_dump: str) -> sourcemap.SourceMap:
  mappings = sourcemap.MappingsGenerator()
  dump_lines: list[str] = mlir_dump.split("\n")

  segment_dict, sources = parse_mlir_locations(dump_lines)
  used_sources = []
  used_sources_filenames = []
  for line in dump_lines:
    mappings.new_group()
    match = LOC_REGEX.search(line)
    if match:
      loc_id = int(match.group("id"))
      if loc_id not in segment_dict:
        # TODO(justinfu): This happens on fusion locations - need to implement.
        continue
      segment = list(segment_dict[loc_id])
      first_col = line.index(line.strip()[0])
      segment[0] = first_col
      # Remap the sourcefile index to only sourcefiles that are used.
      # This is optional but makes the mapping file smaller by pruning
      # unused sourcefiles.
      source_idx = segment[1]
      if source_idx not in used_sources:
        used_sources.append(source_idx)
        used_sources_filenames.append(sources[source_idx])
      segment[1] = used_sources.index(source_idx)
      mappings.new_segment(*segment)
  mappings.new_group()

  return sourcemap.SourceMap(
          version=3,
          sources=used_sources_filenames,
          sources_content=[''] * len(used_sources_filenames),
          mappings=mappings.mappings(),
          names=[],
      )

