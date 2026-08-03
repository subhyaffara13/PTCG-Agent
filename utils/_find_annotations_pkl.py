import re
from pathlib import Path


def _find_annotations_pkl(trace_file: Path) -> Path | None:
    """Auto-discover the annotations pickle from the trace file location.

    Trace files live in e.g. ``traces/step_000000000014/000000.<id>.pt.trace.json.gz``
    where the leading digits are the rank. The pickle lives one level up:
    ``traces/kernel_annotations_rank0_*.pkl``.
    """
    match = re.match(r"^(\d+)", trace_file.name)
    if not match:
        return None
    rank = int(match.group(1))

    traces_dir = trace_file.parent.parent
    candidates = sorted(traces_dir.glob(f"kernel_annotations_rank{rank}_*.pkl"))
    if candidates:
        return candidates[0]
    return None

