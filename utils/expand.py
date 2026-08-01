
def expand(
    image: Image.Image,
    border: int | tuple[int, ...] = 0,
    fill: str | int | tuple[int, ...] = 0,
) -> Image.Image:
    """
    Add border to the image

    :param image: The image to expand.
    :param border: Border width, in pixels.
    :param fill: Pixel fill value (a color value).  Default is 0 (black).
    :return: An image.
    """
    left, top, right, bottom = _border(border)
    width = left + image.size[0] + right
    height = top + image.size[1] + bottom
    color = _color(fill, image.mode)
    if image.palette:
        mode = image.palette.mode
        palette = ImagePalette.ImagePalette(mode, image.getpalette(mode))
        if isinstance(color, tuple) and (len(color) == 3 or len(color) == 4):
            color = palette.getcolor(color)
    else:
        palette = None
    out = Image.new(image.mode, (width, height), color)
    if palette:
        out.putpalette(palette.palette, mode)
    out.paste(image, (left, top))
    return out


def expand(self: list[int], sizes: list[int]):
    if len(sizes) < len(self):
        raise AssertionError(
            f"Expected len(sizes) ({len(sizes)}) >= len(self) ({len(self)})"
        )
    ndim = len(sizes)
    tensor_dim = len(self)
    if ndim == 0:
        return _copy(sizes)
    out: list[int] = []
    for i in range(ndim):
        offset = ndim - 1 - i
        dim = tensor_dim - 1 - offset
        size = self[dim] if dim >= 0 else 1
        targetSize = sizes[i]
        if targetSize == -1:
            if dim < 0:
                raise AssertionError(f"Expected dim ({dim}) >= 0 when targetSize is -1")
            targetSize = size
        if size != targetSize:
            if size != 1:
                raise AssertionError(
                    f"Expected size ({size}) == 1 when size != targetSize ({targetSize})"
                )
            size = targetSize
        out.append(size)
    return out


def expand(x, sizes):
    (x,) = promote_constants([x])
    if isinstance(x, ir.BaseConstant):
        return ExpandView.create(x, tuple(sizes))
    assert isinstance(x, TensorBox)
    assert isinstance(sizes, (list, tuple))
    if tuple(x.get_size()) == tuple(sizes):
        return x

    if not free_unbacked_symbols(x.get_size()):
        x_size_product = V.graph.sizevars.guarding_hint_or_throw(
            sympy_product(x.get_size())
        )
        # TODO: It would be better to realize the input if any of its sizes
        # are unbacked, because typically the size will be non-zero.  However,
        # this cannot be done directly as below as we'll choke on the size_hint
        # here
        if x_size_product > 0 and not free_unbacked_symbols(sizes):
            # maybe realize input before broadcasting it
            x.mark_reuse(
                V.graph.sizevars.guarding_hint_or_throw(sympy_product(sizes))
                // x_size_product
            )
    return TensorBox(ExpandView.create(x.data, tuple(sizes)))


def expand(a: Tensor, *shape, implicit: bool = False) -> Tensor:
    from torch.fx.experimental.symbolic_shapes import (
        guard_or_false,
        guarding_hint_or_throw,
        has_guarding_hint,
        sym_or,
    )

    backed_so = torch.fx.experimental._config.backed_size_oblivious

    # NOTE: cannot use utils.extract_shape_from_varargs here
    # because that also validates the shape, but the shape
    # given to expand may be "invalid"
    if len(shape) == 1 and isinstance(shape[0], Sequence):
        shape = tuple(shape[0])

    torch._check(
        len(shape) >= len(a.shape),
        lambda: "expand: the requested shape has too few dimensions!",
    )

    offset = len(shape) - len(a.shape)
    shape_ = list(shape)
    for idx, x in enumerate(a.shape):
        offset_idx = idx + offset
        requested_length = shape[offset_idx]

        # expand(in -> out) has 3 different semantics:
        # 1) out == -1 -> size = in, stride unchanged
        # 2) in == 1 -> size = out, stride = 0
        # 3) in == out -> size = in, stride unchanged
        #
        # the code below is written for unbacked semantics s.t. we assume unbacked symbols don't
        # represent -1 unless explicitly specified, and the user is opting for case 2) or 3).
        # the sym_or allows either case, but in the decomposition's current state, broadcast_in_dim()
        # will either assume case 3) (via validate_shape() marking the expanded shape size-like), or will
        # raise a data-dependent error trying to figure out if the stride is 0, requiring the user to manually
        # select between the semantics of cases 2) and 3).
        if guard_or_false(requested_length == -1):
            shape_[offset_idx] = x
        else:
            # When backed size oblivious is used, we specialize for broadcasting
            # if its the only way to compile the example input.
            # i.e: x:1, requested_length:1 ==>
            #           assert x==requested_length, no specialization on ==1 or !=1.
            #            The non-broadcast path is picked
            #      x:1, requested_length:4 ==>
            #           specialize(x) to be 1.
            if (
                backed_so
                and has_guarding_hint(x)
                and has_guarding_hint(requested_length)
            ):
                x_hint = guarding_hint_or_throw(x)
                requested_hint = guarding_hint_or_throw(requested_length)
                if x_hint == 1 and requested_hint != 1:
                    torch._check(x == 1)

            torch._check(
                sym_or(x == 1, requested_length == x),
                lambda: f"expand: attempting to expand a dimension of length {x} -> {requested_length}!",
            )
            torch._check(requested_length >= 0)
            shape_[offset_idx] = requested_length

    # At this point shape must be valid
    utils.validate_shape(shape_)

    return prims.broadcast_in_dim(
        a, shape_, tuple(range(offset, len(a.shape) + offset))
    )


def expand(g: jit_utils.GraphContext, self, size, implicit):
    """Implement the expand function for a pytorch tensor in ONNX according to specified `size`"""
    size = symbolic_helper._maybe_get_const(size, "is")
    if not symbolic_helper._is_value(size):
        size = g.op("Constant", value_t=torch.LongTensor(size))
    elif symbolic_helper._is_packed_list(size):
        # Expand with -1 dim value means dim is unchanged.
        # Since onnx::expand supports two-way broadcasting,
        # -1 dim value can be exported to onnx as 1
        size = symbolic_helper._reshape_helper(
            g, stack(g, size, 0), g.op("Constant", value_t=torch.tensor([-1]))
        )
    dtype = _type_utils.JitScalarType.INT64
    ones = ones_like(g, size, dtype)
    neg_ones = mul(g, ones, g.op("Constant", value_t=torch.tensor(-1)))
    size = where(g, g.op("Equal", size, neg_ones), ones, size)
    return g.op("Expand", self, size)


def expand(input_shape: Shape, shape: Shape) -> DimMap:
    """Implement broadcast on multiple dimensions."""
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    if not len(shape) >= len(input_shape):
        raise AssertionError(
            f"Expected len(shape) >= len(input_shape), got {len(shape)} < {len(input_shape)}"
        )

    # 1. create padded input dimensions
    padded_input = dim_pad_left(len(input_shape), len(shape))
    # 2. check that input shapes are compatible
    mapping = []
    for p, desired_s in zip(padded_input, shape):
        if isinstance(p, Singleton):
            actual_s = 1
            if not desired_s >= 0:
                raise AssertionError(f"Expected desired_s >= 0, got {desired_s}")
        else:
            if not isinstance(p, InputDim):
                raise AssertionError(f"DimSpec not supported in expand: {p}")
            actual_s = input_shape[p.input_dim]
            if not (
                guard_or_false(actual_s == 1)
                or guard_or_false(desired_s == -1)
                or guard_or_false(desired_s == actual_s)
            ):
                raise AssertionError(
                    f"Expected actual_s == 1 or desired_s == -1 or "
                    f"desired_s == actual_s, got actual_s={actual_s}, desired_s={desired_s}"
                )
        mapping.append(
            p
            if (
                guard_or_false(desired_s == 1)
                or guard_or_false(desired_s == -1)
                or guard_or_false(desired_s == actual_s)
            )
            else Broadcast.new(p, desired_s)
        )
    return tuple(mapping)


def expand(e, deep=True, modulus=None, power_base=True, power_exp=True,
        mul=True, log=True, multinomial=True, basic=True, **hints):
    r"""
    Expand an expression using methods given as hints.

    Explanation
    ===========

    Hints evaluated unless explicitly set to False are:  ``basic``, ``log``,
    ``multinomial``, ``mul``, ``power_base``, and ``power_exp`` The following
    hints are supported but not applied unless set to True:  ``complex``,
    ``func``, and ``trig``.  In addition, the following meta-hints are
    supported by some or all of the other hints:  ``frac``, ``numer``,
    ``denom``, ``modulus``, and ``force``.  ``deep`` is supported by all
    hints.  Additionally, subclasses of Expr may define their own hints or
    meta-hints.

    The ``basic`` hint is used for any special rewriting of an object that
    should be done automatically (along with the other hints like ``mul``)
    when expand is called. This is a catch-all hint to handle any sort of
    expansion that may not be described by the existing hint names. To use
    this hint an object should override the ``_eval_expand_basic`` method.
    Objects may also define their own expand methods, which are not run by
    default.  See the API section below.

    If ``deep`` is set to ``True`` (the default), things like arguments of
    functions are recursively expanded.  Use ``deep=False`` to only expand on
    the top level.

    If the ``force`` hint is used, assumptions about variables will be ignored
    in making the expansion.

    Hints
    =====

    These hints are run by default

    mul
    ---

    Distributes multiplication over addition:

    >>> from sympy import cos, exp, sin
    >>> from sympy.abc import x, y, z
    >>> (y*(x + z)).expand(mul=True)
    x*y + y*z

    multinomial
    -----------

    Expand (x + y + ...)**n where n is a positive integer.

    >>> ((x + y + z)**2).expand(multinomial=True)
    x**2 + 2*x*y + 2*x*z + y**2 + 2*y*z + z**2

    power_exp
    ---------

    Expand addition in exponents into multiplied bases.

    >>> exp(x + y).expand(power_exp=True)
    exp(x)*exp(y)
    >>> (2**(x + y)).expand(power_exp=True)
    2**x*2**y

    power_base
    ----------

    Split powers of multiplied bases.

    This only happens by default if assumptions allow, or if the
    ``force`` meta-hint is used:

    >>> ((x*y)**z).expand(power_base=True)
    (x*y)**z
    >>> ((x*y)**z).expand(power_base=True, force=True)
    x**z*y**z
    >>> ((2*y)**z).expand(power_base=True)
    2**z*y**z

    Note that in some cases where this expansion always holds, SymPy performs
    it automatically:

    >>> (x*y)**2
    x**2*y**2

    log
    ---

    Pull out power of an argument as a coefficient and split logs products
    into sums of logs.

    Note that these only work if the arguments of the log function have the
    proper assumptions--the arguments must be positive and the exponents must
    be real--or else the ``force`` hint must be True:

    >>> from sympy import log, symbols
    >>> log(x**2*y).expand(log=True)
    log(x**2*y)
    >>> log(x**2*y).expand(log=True, force=True)
    2*log(x) + log(y)
    >>> x, y = symbols('x,y', positive=True)
    >>> log(x**2*y).expand(log=True)
    2*log(x) + log(y)

    basic
    -----

    This hint is intended primarily as a way for custom subclasses to enable
    expansion by default.

    These hints are not run by default:

    complex
    -------

    Split an expression into real and imaginary parts.

    >>> x, y = symbols('x,y')
    >>> (x + y).expand(complex=True)
    re(x) + re(y) + I*im(x) + I*im(y)
    >>> cos(x).expand(complex=True)
    -I*sin(re(x))*sinh(im(x)) + cos(re(x))*cosh(im(x))

    Note that this is just a wrapper around ``as_real_imag()``.  Most objects
    that wish to redefine ``_eval_expand_complex()`` should consider
    redefining ``as_real_imag()`` instead.

    func
    ----

    Expand other functions.

    >>> from sympy import gamma
    >>> gamma(x + 1).expand(func=True)
    x*gamma(x)

    trig
    ----

    Do trigonometric expansions.

    >>> cos(x + y).expand(trig=True)
    -sin(x)*sin(y) + cos(x)*cos(y)
    >>> sin(2*x).expand(trig=True)
    2*sin(x)*cos(x)

    Note that the forms of ``sin(n*x)`` and ``cos(n*x)`` in terms of ``sin(x)``
    and ``cos(x)`` are not unique, due to the identity `\sin^2(x) + \cos^2(x)
    = 1`.  The current implementation uses the form obtained from Chebyshev
    polynomials, but this may change.  See `this MathWorld article
    <https://mathworld.wolfram.com/Multiple-AngleFormulas.html>`_ for more
    information.

    Notes
    =====

    - You can shut off unwanted methods::

        >>> (exp(x + y)*(x + y)).expand()
        x*exp(x)*exp(y) + y*exp(x)*exp(y)
        >>> (exp(x + y)*(x + y)).expand(power_exp=False)
        x*exp(x + y) + y*exp(x + y)
        >>> (exp(x + y)*(x + y)).expand(mul=False)
        (x + y)*exp(x)*exp(y)

    - Use deep=False to only expand on the top level::

        >>> exp(x + exp(x + y)).expand()
        exp(x)*exp(exp(x)*exp(y))
        >>> exp(x + exp(x + y)).expand(deep=False)
        exp(x)*exp(exp(x + y))

    - Hints are applied in an arbitrary, but consistent order (in the current
      implementation, they are applied in alphabetical order, except
      multinomial comes before mul, but this may change).  Because of this,
      some hints may prevent expansion by other hints if they are applied
      first. For example, ``mul`` may distribute multiplications and prevent
      ``log`` and ``power_base`` from expanding them. Also, if ``mul`` is
      applied before ``multinomial`, the expression might not be fully
      distributed. The solution is to use the various ``expand_hint`` helper
      functions or to use ``hint=False`` to this function to finely control
      which hints are applied. Here are some examples::

        >>> from sympy import expand, expand_mul, expand_power_base
        >>> x, y, z = symbols('x,y,z', positive=True)

        >>> expand(log(x*(y + z)))
        log(x) + log(y + z)

      Here, we see that ``log`` was applied before ``mul``.  To get the mul
      expanded form, either of the following will work::

        >>> expand_mul(log(x*(y + z)))
        log(x*y + x*z)
        >>> expand(log(x*(y + z)), log=False)
        log(x*y + x*z)

      A similar thing can happen with the ``power_base`` hint::

        >>> expand((x*(y + z))**x)
        (x*y + x*z)**x

      To get the ``power_base`` expanded form, either of the following will
      work::

        >>> expand((x*(y + z))**x, mul=False)
        x**x*(y + z)**x
        >>> expand_power_base((x*(y + z))**x)
        x**x*(y + z)**x

        >>> expand((x + y)*y/x)
        y + y**2/x

      The parts of a rational expression can be targeted::

        >>> expand((x + y)*y/x/(x + 1), frac=True)
        (x*y + y**2)/(x**2 + x)
        >>> expand((x + y)*y/x/(x + 1), numer=True)
        (x*y + y**2)/(x*(x + 1))
        >>> expand((x + y)*y/x/(x + 1), denom=True)
        y*(x + y)/(x**2 + x)

    - The ``modulus`` meta-hint can be used to reduce the coefficients of an
      expression post-expansion::

        >>> expand((3*x + 1)**2)
        9*x**2 + 6*x + 1
        >>> expand((3*x + 1)**2, modulus=5)
        4*x**2 + x + 1

    - Either ``expand()`` the function or ``.expand()`` the method can be
      used.  Both are equivalent::

        >>> expand((x + 1)**2)
        x**2 + 2*x + 1
        >>> ((x + 1)**2).expand()
        x**2 + 2*x + 1

    API
    ===

    Objects can define their own expand hints by defining
    ``_eval_expand_hint()``.  The function should take the form::

        def _eval_expand_hint(self, **hints):
            # Only apply the method to the top-level expression
            ...

    See also the example below.  Objects should define ``_eval_expand_hint()``
    methods only if ``hint`` applies to that specific object.  The generic
    ``_eval_expand_hint()`` method defined in Expr will handle the no-op case.

    Each hint should be responsible for expanding that hint only.
    Furthermore, the expansion should be applied to the top-level expression
    only.  ``expand()`` takes care of the recursion that happens when
    ``deep=True``.

    You should only call ``_eval_expand_hint()`` methods directly if you are
    100% sure that the object has the method, as otherwise you are liable to
    get unexpected ``AttributeError``s.  Note, again, that you do not need to
    recursively apply the hint to args of your object: this is handled
    automatically by ``expand()``.  ``_eval_expand_hint()`` should
    generally not be used at all outside of an ``_eval_expand_hint()`` method.
    If you want to apply a specific expansion from within another method, use
    the public ``expand()`` function, method, or ``expand_hint()`` functions.

    In order for expand to work, objects must be rebuildable by their args,
    i.e., ``obj.func(*obj.args) == obj`` must hold.

    Expand methods are passed ``**hints`` so that expand hints may use
    'metahints'--hints that control how different expand methods are applied.
    For example, the ``force=True`` hint described above that causes
    ``expand(log=True)`` to ignore assumptions is such a metahint.  The
    ``deep`` meta-hint is handled exclusively by ``expand()`` and is not
    passed to ``_eval_expand_hint()`` methods.

    Note that expansion hints should generally be methods that perform some
    kind of 'expansion'.  For hints that simply rewrite an expression, use the
    .rewrite() API.

    Examples
    ========

    >>> from sympy import Expr, sympify
    >>> class MyClass(Expr):
    ...     def __new__(cls, *args):
    ...         args = sympify(args)
    ...         return Expr.__new__(cls, *args)
    ...
    ...     def _eval_expand_double(self, *, force=False, **hints):
    ...         '''
    ...         Doubles the args of MyClass.
    ...
    ...         If there more than four args, doubling is not performed,
    ...         unless force=True is also used (False by default).
    ...         '''
    ...         if not force and len(self.args) > 4:
    ...             return self
    ...         return self.func(*(self.args + self.args))
    ...
    >>> a = MyClass(1, 2, MyClass(3, 4))
    >>> a
    MyClass(1, 2, MyClass(3, 4))
    >>> a.expand(double=True)
    MyClass(1, 2, MyClass(3, 4, 3, 4), 1, 2, MyClass(3, 4, 3, 4))
    >>> a.expand(double=True, deep=False)
    MyClass(1, 2, MyClass(3, 4), 1, 2, MyClass(3, 4))

    >>> b = MyClass(1, 2, 3, 4, 5)
    >>> b.expand(double=True)
    MyClass(1, 2, 3, 4, 5)
    >>> b.expand(double=True, force=True)
    MyClass(1, 2, 3, 4, 5, 1, 2, 3, 4, 5)

    See Also
    ========

    expand_log, expand_mul, expand_multinomial, expand_complex, expand_trig,
    expand_power_base, expand_power_exp, expand_func, sympy.simplify.hyperexpand.hyperexpand

    """
    # don't modify this; modify the Expr.expand method
    hints['power_base'] = power_base
    hints['power_exp'] = power_exp
    hints['mul'] = mul
    hints['log'] = log
    hints['multinomial'] = multinomial
    hints['basic'] = basic
    return sympify(e).expand(deep=deep, modulus=modulus, **hints)


def expand(values: _ods_ir.Type, filled: _ods_ir.Type, added: _ods_ir.Type, count: _ods_ir.Type, tensor: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return ExpandOp(values=values, filled=filled, added=added, count=count, tensor=tensor, loc=loc, ip=ip).results

