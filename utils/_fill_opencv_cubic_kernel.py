
def _fill_opencv_cubic_kernel(x):
  # See https://github.com/jax-ml/jax/issues/15768#issuecomment-1529939102 and
  # https://en.wikipedia.org/wiki/Bicubic_interpolation#Bicubic_convolution_algorithm
  #
  # When antialiasing is disabled, PyTorch uses a cubic kernel with A = -0.75
  # that matches OpenCV.
  # At least some users consider this a bug (opencv/opencv#17720), and that set
  # of parameters suffers from ringing artifacts.
  a = -0.75
  out = ((a + 2.0) * x - (a + 3.0)) * x * x + 1.0
  out = jnp.where(x >= 1.0, ((a * x - 5.0 * a) * x + 8.0 * a) * x - 4.0 * a,
                  out)
  return jnp.where(x >= 2.0, 0.0, out)

