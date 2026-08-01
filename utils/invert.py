
def invert(image: Image.Image) -> Image.Image:
    """
    Invert an image (channel). ::

        out = MAX - image

    :rtype: :py:class:`~PIL.Image.Image`
    """

    image.load()
    return image._new(image.im.chop_invert())


def invert(image: Image.Image) -> Image.Image:
    """
    Invert (negate) the image.

    :param image: The image to invert.
    :return: An image.
    """
    lut = list(range(255, -1, -1))
    return image.point(lut) if image.mode == "1" else _lut(image, lut)


def invert(x, m):
    """Modular inverse of x modulo m.

    Returns y such that x*y == 1 mod m.

    Uses ``math.pow`` but reproduces the behaviour of ``gmpy2.invert``
    which raises ZeroDivisionError if no inverse exists.
    """
    try:
        return pow(x, -1, m)
    except ValueError:
        raise ZeroDivisionError("invert() no inverse exists")


def invert(f, g, *gens, **args):
    """
    Invert ``f`` modulo ``g`` when possible.

    Examples
    ========

    >>> from sympy import invert, S, mod_inverse
    >>> from sympy.abc import x

    >>> invert(x**2 - 1, 2*x - 1)
    -4/3

    >>> invert(x**2 - 1, x - 1)
    Traceback (most recent call last):
    ...
    NotInvertible: zero divisor

    For more efficient inversion of Rationals,
    use the :obj:`sympy.core.intfunc.mod_inverse` function:

    >>> mod_inverse(3, 5)
    2
    >>> (S(2)/5).invert(S(7)/3)
    5/2

    See Also
    ========
    sympy.core.intfunc.mod_inverse

    """
    options.allowed_flags(args, ['auto', 'polys'])

    try:
        (F, G), opt = parallel_poly_from_expr((f, g), *gens, **args)
    except PolificationFailed as exc:
        domain, (a, b) = construct_domain(exc.exprs)

        try:
            return domain.to_sympy(domain.invert(a, b))
        except NotImplementedError:
            raise ComputationFailed('invert', 2, exc)

    h = F.invert(G, auto=opt.auto)

    if not opt.polys:
        return h.as_expr()
    else:
        return h


def invert(x: ArrayLike, /) -> Array:
  """Compute the bitwise inversion of an input.

  JAX implementation of :func:`numpy.invert`. This function provides the
  implementation of the ``~`` operator for JAX arrays.

  Args:
    x: input array, must be boolean or integer typed.

  Returns:
    An array of the same shape and dtype as ```x``, with the bits inverted.

  See also:
    - :func:`jax.numpy.bitwise_invert`: Array API alias of this function.
    - :func:`jax.numpy.logical_not`: Invert after casting input to boolean.

  Examples:
    >>> x = jnp.arange(5, dtype='uint8')
    >>> print(x)
    [0 1 2 3 4]
    >>> print(jnp.invert(x))
    [255 254 253 252 251]

    This function implements the unary ``~`` operator for JAX arrays:

    >>> print(~x)
    [255 254 253 252 251]

    :func:`invert` operates bitwise on the input, and so the meaning of its
    output may be more clear by showing the bitwise representation:

    >>> with jnp.printoptions(formatter={'int': lambda x: format(x, '#010b')}):
    ...   print(f"{x  = }")
    ...   print(f"{~x = }")
    x  = Array([0b00000000, 0b00000001, 0b00000010, 0b00000011, 0b00000100], dtype=uint8)
    ~x = Array([0b11111111, 0b11111110, 0b11111101, 0b11111100, 0b11111011], dtype=uint8)

    For boolean inputs, :func:`invert` is equivalent to :func:`logical_not`:

    >>> x = jnp.array([True, False, True, True, False])
    >>> jnp.invert(x)
    Array([False,  True, False, False,  True], dtype=bool)
  """
  return lax.bitwise_not(*promote_args('invert', x))

