
def format_frames(frames: list[dict[str, str]]) -> str:
    formatted_frames = []
    for frame in frames:
        formatted_frames.append(format_frame(frame))
    return "\n".join(formatted_frames)

