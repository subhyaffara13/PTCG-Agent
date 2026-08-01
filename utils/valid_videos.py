
def valid_videos(videos):
    # If we have a list of videos, it could be either one video as list of frames or a batch
    if isinstance(videos, (list, tuple)):
        for video_or_frame in videos:
            if not (is_valid_video(video_or_frame) or is_valid_video_frame(video_or_frame)):
                return False
    # If not a list, then we have a single 4D video or 5D batched tensor
    elif not is_valid_video(videos) or videos.ndim == 5:
        return False
    return True

