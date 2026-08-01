
def parse_mlir_locations(
    mlir_dump: list[str],
) -> tuple[dict[int, sourcemap.Segment], list[str]]:
  locations: dict[int, Location | Redirect] = {}
  source_files = []
  for line in mlir_dump:
    if line.startswith("#loc"):
      src_match = SRC_REGEX.match(line)
      if src_match:
        match_dict = src_match.groupdict()
        filename = match_dict["file"]
        locations[int(match_dict["id"])] = Location(
            file=filename,
            line=int(match_dict["line"]),
            col=int(match_dict["col"]),
        )
        if filename not in source_files:
          source_files.append(filename)
        continue
      scoped_match = SCOPED_REGEX.match(line)
      if scoped_match:
        match_dict = scoped_match.groupdict()
        locations[int(match_dict["id"])] = Redirect(
            tgt_id=int(match_dict["tgt_id"])
        )
        continue
      callsite_match = CALLSITE_REGEX.match(line)
      if callsite_match:
        match_dict = callsite_match.groupdict()
        locations[int(match_dict["id"])] = Redirect(
            tgt_id=int(match_dict["callee"])
        )
        continue
      if "loc(unknown)" in line:
        continue
  # Resolve redirects
  while True:
    new_locations: dict[int, Location | Redirect] = {}
    updated = False
    for loc_id, loc in locations.items():
      if isinstance(loc, Redirect):
        new_locations[loc_id] = locations[loc.tgt_id]
        updated = True
      else:
        new_locations[loc_id] = loc
    locations = new_locations
    if not updated:
      break
  segment_dict: dict[int, sourcemap.Segment] = {}
  for id_, loc in locations.items():
    # A segment is a tuple of the form:
    # (generated_col, src_file_idx, src_line, src_col)
    loc = cast(Location, loc)
    segment_dict[id_] = (
        0,
        source_files.index(loc.file),
        loc.line - 1,  # Zero-indexed, so offset by 1.
        loc.col,
    )
  return segment_dict, source_files

