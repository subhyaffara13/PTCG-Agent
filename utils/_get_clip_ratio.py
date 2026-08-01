
def _get_clip_ratio(clip_start: float, clip_end: float, progress: float) -> float:
    return clip_start + (clip_end - clip_start) * progress

