
def rotate(th):
    """Return the matrix to rotate a 2-D point about the origin by ``angle``.

    The angle is measured in radians. To Point a point about a point other
    then the origin, translate the Point, do the rotation, and
    translate it back:

    >>> from sympy.geometry.entity import rotate, translate
    >>> from sympy import Point, pi
    >>> rot_about_11 = translate(-1, -1)*rotate(pi/2)*translate(1, 1)
    >>> Point(1, 1).transform(rot_about_11)
    Point2D(1, 1)
    >>> Point(0, 0).transform(rot_about_11)
    Point2D(2, 0)
    """
    s = sin(th)
    rv = eye(3)*cos(th)
    rv[0, 1] = s
    rv[1, 0] = -s
    rv[2, 2] = 1
    return rv


def rotate(input, angle, axes=(1, 0), reshape=True, output=None, order=3,
           mode='constant', cval=0.0, prefilter=True):
    """
    Rotate an array.

    The array is rotated in the plane defined by the two axes given by the
    `axes` parameter using spline interpolation of the requested order.

    Parameters
    ----------
    %(input)s
    angle : float
        The rotation angle in degrees.
    axes : tuple of 2 ints, optional
        The two axes that define the plane of rotation. Default is the first
        two axes.
    reshape : bool, optional
        If `reshape` is true, the output shape is adapted so that the input
        array is contained completely in the output. Default is True.
    %(output)s
    order : int, optional
        The order of the spline interpolation, default is 3.
        The order has to be in the range 0-5.
    %(mode_interp_constant)s
    %(cval)s
    %(prefilter)s

    Returns
    -------
    rotate : ndarray
        The rotated input.

    Notes
    -----
    For complex-valued `input`, this function rotates the real and imaginary
    components independently.

    .. versionadded:: 1.6.0
        Complex-valued support added.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure(figsize=(10, 3))
    >>> ax1, ax2, ax3 = fig.subplots(1, 3)
    >>> img = datasets.ascent()
    >>> img_45 = ndimage.rotate(img, 45, reshape=False)
    >>> full_img_45 = ndimage.rotate(img, 45, reshape=True)
    >>> ax1.imshow(img, cmap='gray')
    >>> ax1.set_axis_off()
    >>> ax2.imshow(img_45, cmap='gray')
    >>> ax2.set_axis_off()
    >>> ax3.imshow(full_img_45, cmap='gray')
    >>> ax3.set_axis_off()
    >>> fig.set_layout_engine('tight')
    >>> plt.show()
    >>> print(img.shape)
    (512, 512)
    >>> print(img_45.shape)
    (512, 512)
    >>> print(full_img_45.shape)
    (724, 724)

    """
    input_arr = np.asarray(input)
    ndim = input_arr.ndim

    if ndim < 2:
        raise ValueError('input array should be at least 2D')

    axes = list(axes)

    if len(axes) != 2:
        raise ValueError('axes should contain exactly two values')

    if not all([float(ax).is_integer() for ax in axes]):
        raise ValueError('axes should contain only integer values')

    if axes[0] < 0:
        axes[0] += ndim
    if axes[1] < 0:
        axes[1] += ndim
    if axes[0] < 0 or axes[1] < 0 or axes[0] >= ndim or axes[1] >= ndim:
        raise ValueError('invalid rotation plane specified')

    axes.sort()

    c, s = special.cosdg(angle), special.sindg(angle)

    rot_matrix = np.array([[c, s],
                           [-s, c]])

    img_shape = np.asarray(input_arr.shape)
    in_plane_shape = img_shape[axes]
    if reshape:
        # Compute transformed input bounds
        iy, ix = in_plane_shape
        out_bounds = rot_matrix @ [[0, 0, iy, iy],
                                   [0, ix, 0, ix]]
        # Compute the shape of the transformed input plane
        out_plane_shape = (np.ptp(out_bounds, axis=1) + 0.5).astype(int)
    else:
        out_plane_shape = img_shape[axes]

    out_center = rot_matrix @ ((out_plane_shape - 1) / 2)
    in_center = (in_plane_shape - 1) / 2
    offset = in_center - out_center

    output_shape = img_shape
    output_shape[axes] = out_plane_shape
    output_shape = tuple(output_shape)

    complex_output = np.iscomplexobj(input_arr)
    output = _ni_support._get_output(output, input_arr, shape=output_shape,
                                     complex_output=complex_output)

    if ndim <= 2:
        affine_transform(input_arr, rot_matrix, offset, output_shape, output,
                         order, mode, cval, prefilter)
    else:
        # If ndim > 2, the rotation is applied over all the planes
        # parallel to axes
        planes_coord = itertools.product(
            *[[slice(None)] if ax in axes else range(img_shape[ax])
              for ax in range(ndim)])

        out_plane_shape = tuple(out_plane_shape)

        for coordinates in planes_coord:
            ia = input_arr[coordinates]
            oa = output[coordinates]
            affine_transform(ia, rot_matrix, offset, out_plane_shape,
                             oa, order, mode, cval, prefilter)

    return output


def rotate(matrix, angle, x, y, z):
    """
    Rotate a matrix around an axis.

    :param matrix: The matrix to rotate.
    :param angle: The angle to rotate by.
    :param x: x of axis to rotate around.
    :param y: y of axis to rotate around.
    :param z: z of axis to rotate around.

    :return: The rotated matrix
    """
    angle = math.pi * angle / 180
    c, s = math.cos(angle), math.sin(angle)
    n = math.sqrt(x * x + y * y + z * z)
    x, y, z = x / n, y / n, z / n
    cx, cy, cz = (1 - c) * x, (1 - c) * y, (1 - c) * z
    rotation_matrix = array(
        [
            [cx * x + c, cy * x - z * s, cz * x + y * s, 0],
            [cx * y + z * s, cy * y + c, cz * y - x * s, 0],
            [cx * z - y * s, cy * z + x * s, cz * z + c, 0],
            [0, 0, 0, 1],
        ],
        dtype=matrix.dtype,
    ).T
    matrix[...] = dot(matrix, rotation_matrix)
    return matrix


def rotate(value: _ods_ir.Value, offset: _Union[int, _ods_ir.IntegerAttr], width: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return RotateOp(value=value, offset=offset, width=width, results=results, loc=loc, ip=ip).results

