import json

def get_profiler_nccl_meta(prof):
    """Torch profiler includes nccl metadata in an inserted operator called "record_param_comms"
    We will need to test metadata obtained from profiler here"""
    with TemporaryFileName(mode="w+t", suffix=".json") as trace_file:
        prof.export_chrome_trace(trace_file)
        with open(trace_file) as f:
            events = json.load(f)["traceEvents"]
        print(f"Trace saved to {trace_file}")

        return [e for e in events if e.get("name") == "record_param_comms"]

