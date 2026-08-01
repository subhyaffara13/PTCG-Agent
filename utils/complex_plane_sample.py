
def complex_plane_sample(dtype, size_re=10, size_im=None):
  """Return a 2-D array of complex numbers that covers the complex plane
     with a grid of samples.

     The size of the grid is (3 + 2 * size_im) x (3 + 2 * size_re)
     that includes infinity points, extreme finite points, and the
     specified number of points from real and imaginary axis.

     For example:

     >>> print(complex_plane_sample(np.complex64, 0, 3))
     [[-inf          -infj   0.          -infj  inf          -infj]
      [-inf-3.4028235e+38j   0.-3.4028235e+38j  inf-3.4028235e+38j]
      [-inf-2.0000000e+00j   0.-2.0000000e+00j  inf-2.0000000e+00j]
      [-inf-1.1754944e-38j   0.-1.1754944e-38j  inf-1.1754944e-38j]
      [-inf+0.0000000e+00j   0.+0.0000000e+00j  inf+0.0000000e+00j]
      [-inf+1.1754944e-38j   0.+1.1754944e-38j  inf+1.1754944e-38j]
      [-inf+2.0000000e+00j   0.+2.0000000e+00j  inf+2.0000000e+00j]
      [-inf+3.4028235e+38j   0.+3.4028235e+38j  inf+3.4028235e+38j]
      [-inf          +infj   0.          +infj  inf          +infj]]

  """
  if size_im is None:
    size_im = size_re
  finfo = np.finfo(dtype)

  machine = platform.machine()
  is_arm_cpu = machine.startswith('aarch') or machine.startswith('arm')
  smallest = np.nextafter(finfo.tiny, finfo.max) if is_arm_cpu and platform.system() == 'Darwin' else finfo.tiny

  def make_axis_points(size):
    prec_dps_ratio = 3.3219280948873626
    logmin = finfo.maxexp / prec_dps_ratio
    logtiny = finfo.minexp / prec_dps_ratio
    axis_points = np.zeros(3 + 2 * size, dtype=finfo.dtype)

    with ignore_warning(category=RuntimeWarning):
      # Silence RuntimeWarning: overflow encountered in cast
      half_neg_line = -np.logspace(logmin, logtiny, size, dtype=finfo.dtype)
      half_line = -half_neg_line[::-1]
      axis_points[-size - 1:-1] = half_line
      axis_points[1:size + 1] = half_neg_line

    if size > 1:
      axis_points[1] = finfo.min
      axis_points[-2] = finfo.max
    if size > 0:
      axis_points[size] = -smallest
      axis_points[-size - 1] = smallest
    axis_points[0] = -np.inf
    axis_points[-1] = np.inf
    return axis_points

  real_axis_points = make_axis_points(size_re)
  imag_axis_points = make_axis_points(size_im)

  real_part = real_axis_points.reshape((-1, 3 + 2 * size_re)).repeat(3 + 2 * size_im, 0).astype(dtype)

  imag_part = imag_axis_points.repeat(2).view(dtype)
  imag_part.real[:] = 0
  imag_part = imag_part.reshape((3 + 2 * size_im, -1)).repeat(3 + 2 * size_re, 1)

  return real_part + imag_part

