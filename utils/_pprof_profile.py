import itertools
import json
import re

def _pprof_profile(
    profile: dict[tuple[xla_client.Traceback | None, core.Primitive], int],
    workspace_root: str | None = None,
    *,
    sample_type: str,
    sample_unit: str,
    comment: str = "",
) -> bytes:
  """Converts a profile into a compressed pprof protocol buffer.

  The input profile is a map from (traceback, primitive) pairs to counts.
  """
  s: defaultdict[str, int]
  func: defaultdict[types.CodeType, int]
  loc: defaultdict[tuple[types.CodeType, int], int]

  s = defaultdict(itertools.count(1).__next__)
  func = defaultdict(itertools.count(1).__next__)
  loc = defaultdict(itertools.count(1).__next__)
  s[""] = 0
  primitive_key = s["primitive"]
  samples = []
  for (tb, primitive), count in profile.items():
    if tb is None:
      frames = []
    else:
      raw_frames = zip(*tb.raw_frames())
      frames = [loc[(code, lasti)] for code, lasti in raw_frames
                if source_info_util.is_user_filename(code.co_filename)]
    samples.append({
       "location_id": frames,
       "value": [count],
       "label": [{
         "key": primitive_key,
         "str": s[primitive.name]
        }]
    })

  locations = [
      {"id": loc_id,
       "line": [{"function_id": func[code],
                 "line": xla_client.Traceback.code_addr2line(code, lasti)}]}
      for (code, lasti), loc_id in loc.items()
  ]
  functions = []
  for code, func_id in func.items():
    filename = code.co_filename
    name = code.co_qualname
    if workspace_root is not None:
      filename = _strip_workspace_root(filename, workspace_root)
    else:
      pattern = config.hlo_source_file_canonicalization_regex.value
      if pattern:
        filename = re.sub(pattern, '', filename)
    name = f"{filename.removesuffix('.py').replace('/', '.')}.{name}"
    functions.append({
        "id": func_id,
        "name": s[name],
        "filename": s[filename],
        "start_line": code.co_firstlineno,
    })
  # This is the JSON encoding of a pprof profile protocol buffer. See:
  # https://github.com/google/pprof/blob/master/proto/profile.proto for a
  # description of the format.
  sample_type_id = s[sample_type]
  sample_unit_id = s[sample_unit]
  comment_id = s[comment]
  json_profile = json.dumps({
      "string_table": list(s.keys()),
      "location": locations,
      "function": functions,
      "sample_type": [{"type": sample_type_id, "unit": sample_unit_id}],
      "sample": samples,
      "comment": comment_id,
  })
  return gzip.compress(_jax.json_to_pprof_profile(json_profile))

