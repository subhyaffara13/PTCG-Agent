from typing import Any

def get_sorted_gpu_mm_conv_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def is_mm_conv_event(event: dict[str, Any]) -> bool:
        return "name" in event and (
            "gemm" in event["name"]
            or "conv" in event["name"]
            or "cutlass" in event["name"]
            or "wgrad" in event["name"]
        )

    gpu_events = get_sorted_gpu_events(events)
    sorted_events: list[dict[str, Any]] = []
    for event in gpu_events:
        if not is_mm_conv_event(event):
            continue
        sorted_events.append(event)
    return sorted_events

