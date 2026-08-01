
def is_scaled_video(video: np.ndarray) -> bool:
    """
    Checks to see whether the pixel values have already been rescaled to [0, 1].
    """
    # It's possible the video has pixel values in [0, 255] but is of floating type
    return np.min(video) >= 0 and np.max(video) <= 1

