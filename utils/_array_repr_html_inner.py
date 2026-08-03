from typing import Any, Optional

def _array_repr_html_inner(
    img: Array,
    *,
    # If updating this, also update `auto_plot_array` !!!
    video_min_num_frames: int = 15,
    height: None | int | tuple[int, int] = (100, 250),
    show_images_kwargs: Optional[dict[str, Any]] = None,
    show_videos_kwargs: Optional[dict[str, Any]] = None,
) -> Optional[str]:
  """Display the normalized img, or `None` if the input is not an image."""
  show_images_kwargs = show_images_kwargs or {}
  show_videos_kwargs = show_videos_kwargs or {}

  if not enp.lazy.is_array(img):  # Not an array
    return None

  # Normalize tf.Tensor into np.array
  if enp.lazy.is_tf(img) or enp.lazy.is_torch(img):
    img = img.numpy()

  shape = img.shape
  ndim = len(shape)

  # Infer the array type (image or video ?)
  if ndim == 2:
    img_shape = shape
    num_channel = 1
  elif ndim == 3:
    img_shape = shape[:2]
    num_channel = shape[-1]
  elif ndim == 4:
    img_shape = shape[1:3]
    num_channel = shape[-1]
    num_frames = shape[0]
  else:
    return None

  # Filter non-images
  if 0 in shape:  # Empty image
    return None
  if _smaller_than(img_shape, _MIN_IMG_SHAPE):
    return None
  if num_channel not in {1, 3, 4}:
    return None

  show_images_kwargs = show_images_kwargs.copy()
  show_videos_kwargs = show_videos_kwargs.copy()

  # Resize small/large images to X pixels (otherwise, difficult to see)
  if height:
    if isinstance(height, int):
      min_height = height
      max_height = height
    else:
      min_height, max_height = height
    del height
    target_height = img_shape[0]  # (h, w)
    target_height = max(target_height, min_height)
    target_height = min(target_height, max_height)

    show_images_kwargs.setdefault('height', target_height)
    show_videos_kwargs.setdefault('height', target_height)

  if ndim < 4:
    out = media.show_image(img, return_html=True, **show_images_kwargs)
  elif num_frames < video_min_num_frames:
    out = media.show_images(img, return_html=True, **show_images_kwargs)
  else:
    # TODO(epot): media.show_video does not support single channel video
    if num_channel != 3:
      return None
    # Dynamically compute the frame-rate, capped at 25 FPS
    fps = min(num_frames // 5, 25.0)

    show_videos_kwargs.setdefault('fps', fps)

    out = media.show_video(
        img,
        return_html=True,
        **show_videos_kwargs,
    )
  return out

