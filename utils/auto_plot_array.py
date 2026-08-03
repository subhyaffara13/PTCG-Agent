import functools
from typing import Any, Optional

def auto_plot_array(
    *,
    # If updating this, also update `_array_repr_html_inner` !!!
    video_min_num_frames: int = 15,
    # Images outside this range are rescalled
    height: None | int | tuple[int, int] = (100, 250),
    show_images_kwargs: Optional[dict[str, Any]] = None,
    show_videos_kwargs: Optional[dict[str, Any]] = None,
) -> None:
  """If called, 2d/3d imgage arrays will be plotted as images in colab/jupyter.

  Usage:

  >>> ecolab.auto_plot_array()
  >>> np.zeros((28, 28, 3))  # Displayed as image

  Args:
    video_min_num_frames: Video `(num_frames, h, w, c)` with less than this
      number of frames will be displayed as individual images
    height: `(min, max)` image height in pixels. Images smaller/larger will be
      reshaped. `None` to disable. If a single number, assume `min == max`.
    show_images_kwargs: Kwargs forwarded to `mediapy.show_images`
    show_videos_kwargs: Kwargs forwarded to `mediapy.show_videos`
  """

  ipython = IPython.get_ipython()
  if ipython is None:
    return  # Non-notebook environement

  array_repr_html_fn = functools.partial(
      array_repr_html,
      video_min_num_frames=video_min_num_frames,
      height=height,
      show_images_kwargs=show_images_kwargs,
      show_videos_kwargs=show_videos_kwargs,
  )

  # Register the new representation fo np, tf and jax array
  print('Display big np/tf/jax arrays as image for nicer IPython display')
  formatter = ipython.display_formatter.formatters['text/html']

  # TODO(epot): How to support lazy-imports without catching everything ?
  # Try registering jax
  try:
    jnp = enp.lazy.jnp
  except ImportError:
    pass
  else:
    # The array type is not exposed in the public API (registering jnp.ndarray
    # does not works), so dynamically extracting the type
    jax_array_cls = type(jnp.zeros(shape=()))  # DeviceArrayBase
    formatter.for_type(jax_array_cls, array_repr_html_fn)

  # Try registering TF
  try:
    tf = enp.lazy.tf
  except ImportError:
    pass
  else:
    formatter.for_type(tf.Tensor, array_repr_html_fn)

  # Try registering Torch
  try:
    torch = enp.lazy.torch
  except ImportError:
    pass
  else:
    formatter.for_type(torch.Tensor, array_repr_html_fn)

  # Register np
  formatter.for_type(enp.lazy.np.ndarray, array_repr_html_fn)

