
def is_valid_video(video):
    if not isinstance(video, (list, tuple)):
        return (is_numpy_array(video) or is_torch_tensor(video)) and video.ndim == 4
    return video and all(is_valid_video_frame(frame) for frame in video)

