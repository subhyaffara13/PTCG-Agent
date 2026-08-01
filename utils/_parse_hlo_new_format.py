
def _parse_hlo_new_format(lines: list[str]) -> sourcemap.SourceMap:
  file_names = {}
  file_locations = {}
  stack_frames = {}
  current_section = None
  for line in lines:
    line = line.strip()
    if not line:
      continue

    if line in ["FileNames", "FunctionNames", "FileLocations", "StackFrames"]:
      current_section = line
      continue

    if current_section == "FileNames":
      match = re.match(r"(\d+)\s+\"(.*)\"", line)
      if match:
        file_names[int(match.group(1))] = match.group(2)
    elif current_section == "FileLocations":
      # Format: 1 {file_name_id=1 function_name_id=1 line=153 end_line=153 column=2 end_column=31}
      match = re.match(r"(\d+)\s+{(.*)}", line)
      if match:
        loc_id = int(match.group(1))
        attrs = match.group(2)
        loc_data = {}
        for part in attrs.split():
          if "=" in part:
            k, v = part.split("=")
            if k not in ["file_name_id", "function_name_id", "line",
                         "end_line", "column", "end_column"]:
              raise ValueError(f"Unknown attribute for FileLocations: {k}")
            loc_data[k] = int(v)
        file_locations[loc_id] = loc_data
    elif current_section == "StackFrames":
      # Format: 1 {file_location_id=1 parent_frame_id=1}
      match = re.match(r"(\d+)\s+{(.*)}", line)
      if match:
        frame_id = int(match.group(1))
        attrs = match.group(2)
        frame_data = {}
        for part in attrs.split():
          if "=" in part:
            k, v = part.split("=")
            if k not in ["file_location_id", "parent_frame_id"]:
              raise ValueError(f"Unknown attribute for StackFrames: {k}")
            frame_data[k] = int(v)
        stack_frames[frame_id] = frame_data

  mappings = sourcemap.MappingsGenerator()
  used_source_files = []

  for line in lines:
    mappings.new_group()
    if "metadata={" in line:
      match = re.search(r"stack_frame_id=(\d+)", line)
      if match:
        stack_frame_id = int(match.group(1))
        if stack_frame_id in stack_frames:
          frame = stack_frames[stack_frame_id]
          file_loc = file_locations.get(frame["file_location_id"])
          if file_loc:
            file_name = file_names.get(file_loc["file_name_id"])
            if file_name:
              if file_name not in used_source_files:
                used_source_files.append(file_name)
              src_file_idx = used_source_files.index(file_name)
              src_line = file_loc["line"] - 1
              first_col = line.index(line.strip()[0])
              mappings.new_segment(first_col, src_file_idx, src_line, 0)
          else:
            raise ValueError(f"Could not find mapping for {file_loc=}")
        else:
          raise ValueError(f"Could not find mapping for {stack_frame_id=}")
  mappings.new_group()
  return sourcemap.SourceMap(
      version=3,
      sources=used_source_files,
      sources_content=[],
      mappings=mappings.mappings(),
      names=[],
  )

