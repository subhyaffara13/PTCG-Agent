
def scale(
    image: Image.Image, factor: float, resample: int = Image.Resampling.BICUBIC
) -> Image.Image:
    """
    Returns a rescaled image by a specific factor given in parameter.
    A factor greater than 1 expands the image, between 0 and 1 contracts the
    image.

    :param image: The image to rescale.
    :param factor: The expansion factor, as a float.
    :param resample: Resampling method to use. Default is
                     :py:attr:`~PIL.Image.Resampling.BICUBIC`.
                     See :ref:`concept-filters`.
    :returns: An :py:class:`~PIL.Image.Image` object.
    """
    if factor == 1:
        return image.copy()
    elif factor <= 0:
        msg = "the factor must be greater than 0"
        raise ValueError(msg)
    else:
        size = (round(factor * image.width), round(factor * image.height))
        return image.resize(size, resample)


def scale(x, y, pt=None):
    """Return the matrix to multiply a 2-D point's coordinates by x and y.

    If pt is given, the scaling is done relative to that point."""
    rv = eye(3)
    rv[0, 0] = x
    rv[1, 1] = y
    if pt:
        from sympy.geometry.point import Point
        pt = Point(pt, dim=2)
        tr1 = translate(*(-pt).args)
        tr2 = translate(*pt.args)
        return tr1*rv*tr2
    return rv


def scale(
    sample: "npt.ArrayLike",
    l_bounds: "npt.ArrayLike",
    u_bounds: "npt.ArrayLike",
    *,
    reverse: bool = False
) -> np.ndarray:
    r"""Sample scaling from unit hypercube to different bounds.

    To convert a sample from :math:`[0, 1)` to :math:`[a, b), b>a`,
    with :math:`a` the lower bounds and :math:`b` the upper bounds.
    The following transformation is used:

    .. math::

        (b - a) \cdot \text{sample} + a

    Parameters
    ----------
    sample : array_like (n, d)
        Sample to scale.
    l_bounds, u_bounds : array_like (d,)
        Lower and upper bounds (resp. :math:`a`, :math:`b`) of transformed
        data. If `reverse` is True, range of the original data to transform
        to the unit hypercube.
    reverse : bool, optional
        Reverse the transformation from different bounds to the unit hypercube.
        Default is False.

    Returns
    -------
    sample : array_like (n, d)
        Scaled sample.

    Examples
    --------
    Transform 3 samples in the unit hypercube to bounds:

    >>> from scipy.stats import qmc
    >>> l_bounds = [-2, 0]
    >>> u_bounds = [6, 5]
    >>> sample = [[0.5 , 0.75],
    ...           [0.5 , 0.5],
    ...           [0.75, 0.25]]
    >>> sample_scaled = qmc.scale(sample, l_bounds, u_bounds)
    >>> sample_scaled
    array([[2.  , 3.75],
           [2.  , 2.5 ],
           [4.  , 1.25]])

    And convert back to the unit hypercube:

    >>> sample_ = qmc.scale(sample_scaled, l_bounds, u_bounds, reverse=True)
    >>> sample_
    array([[0.5 , 0.75],
           [0.5 , 0.5 ],
           [0.75, 0.25]])

    """
    sample = np.asarray(sample)

    # Checking bounds and sample
    if not sample.ndim == 2:
        raise ValueError('Sample is not a 2D array')

    lower, upper = _validate_bounds(
        l_bounds=l_bounds, u_bounds=u_bounds, d=sample.shape[1]
    )

    if not reverse:
        # Checking that sample is within the hypercube
        if (sample.max() > 1.) or (sample.min() < 0.):
            raise ValueError('Sample is not in unit hypercube')

        return sample * (upper - lower) + lower
    else:
        # Checking that sample is within the bounds
        if not (np.all(sample >= lower) and np.all(sample <= upper)):
            raise ValueError('Sample is out of bounds')

        return (sample - lower) / (upper - lower)


def scale(step_size: jax.typing.ArrayLike) -> base.GradientTransformation:
  """Scale updates by some fixed scalar `step_size`.

  Args:
    step_size: A scalar corresponding to a fixed scaling factor for updates.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def update_fn(updates, state, params=None):
    del params
    updates = jax.tree.map(lambda g: step_size * g, updates)
    return updates, state

  return base.GradientTransformation(base.init_empty_state, update_fn)


def Scale(x: float, y: float | None = None) -> Transform:
    """Return the identity transformation scaled by x, y. The 'y' argument
    may be None, which implies to use the x value for y as well.

    :Example:
            >>> Scale(2, 3)
            <Transform [2 0 0 3 0 0]>
            >>>
    """
    if y is None:
        y = x
    return Transform(x, 0, 0, y, 0, 0)

