
def _fill_keys_cubic_kernel(x):
  # http://ieeexplore.ieee.org/document/1163711/
  # R. G. Keys. Cubic convolution interpolation for digital image processing.
  # IEEE Transactions on Acoustics, Speech, and Signal Processing,
  # 29(6):1153–1160, 1981.
  #
  # https://en.wikipedia.org/wiki/Bicubic_interpolation#Bicubic_convolution_algorithm
  # This is the Keys kernel with A=-0.5.
  #
  # This kernel matches Pillow, TensorFlow, and Pytorch when
  # antialiasing is enabled.
  out = ((1.5 * x - 2.5) * x) * x + 1.
  out = jnp.where(x >= 1., ((-0.5 * x + 2.5) * x - 4.) * x + 2., out)
  return jnp.where(x >= 2., 0., out)

