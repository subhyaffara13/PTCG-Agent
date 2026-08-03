import json
import os
import pathlib

def _write_perfetto_trace_file(log_dir: os.PathLike | str):
  # Navigate to folder with the latest trace dump to find `trace.json.jz`
  trace_folders = (pathlib.Path(log_dir).absolute() / "plugins" / "profile").iterdir()
  latest_trace_folder = max(trace_folders, key=os.path.getmtime)
  trace_jsons = latest_trace_folder.glob("*.trace.json.gz")
  try:
    trace_json, = trace_jsons
  except ValueError as value_error:
    raise ValueError(f"Invalid trace folder: {latest_trace_folder}") from value_error

  logger.info("Loading trace.json.gz and removing its metadata...")
  # Perfetto doesn't like the `metadata` field in `trace.json` so we remove
  # it.
  # TODO(sharadmv): speed this up by updating the generated `trace.json`
  # to not include metadata if possible.
  with gzip.open(trace_json, "rb") as fp:
    trace = json.load(fp)
    del trace["metadata"]
  perfetto_trace = latest_trace_folder / "perfetto_trace.json.gz"
  logger.info("Writing perfetto_trace.json.gz...")
  with gzip.open(perfetto_trace, "w") as fp:
    fp.write(json.dumps(trace).encode("utf-8"))
  return perfetto_trace

