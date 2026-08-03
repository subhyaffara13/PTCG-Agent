from typing import Any

def format_tb(frames: list[Any]) -> str:
    formatted_traceback = [
        traceback.FrameSummary(entry["filename"], entry["line"], entry["name"])
        for entry in frames
    ]

    return "".join(traceback.format_list(formatted_traceback))

