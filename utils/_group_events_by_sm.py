import re
from typing import Any

def _group_events_by_sm(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Group events so all CTAs on the same SM share one track.

    Transforms:
    - pid: "Core0 CTA6" -> "Core0"
    - tid: "warp0" -> "CTA6 warp0"
    """
    core_cta_pattern = re.compile(r"^(.*?)\s*(Core\d+)\s+(CTA\d+)$")

    for event in events:
        pid = event.get("pid", "")
        tid = event.get("tid", "")

        match = core_cta_pattern.match(str(pid))
        if match:
            prefix = match.group(1).strip()
            core = match.group(2)
            cta = match.group(3)
            event["pid"] = f"{prefix} {core}" if prefix else core
            event["tid"] = f"{cta} {tid}" if tid else cta

    return events

