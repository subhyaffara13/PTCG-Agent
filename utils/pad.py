
def pad(
    image: Image.Image,
    size: tuple[int, int],
    method: int = Image.Resampling.BICUBIC,
    color: str | int | tuple[int, ...] | None = None,
    centering: tuple[float, float] = (0.5, 0.5),
) -> Image.Image:
    """
    Returns a resized and padded version of the image, expanded to fill the
    requested aspect ratio and size.

    :param image: The image to resize and crop.
    :param size: The requested output size in pixels, given as a
                 (width, height) tuple.
    :param method: Resampling method to use. Default is
                   :py:attr:`~PIL.Image.Resampling.BICUBIC`.
                   See :ref:`concept-filters`.
    :param color: The background color of the padded image.
    :param centering: Control the position of the original image within the
                      padded version.

                          (0.5, 0.5) will keep the image centered
                          (0, 0) will keep the image aligned to the top left
                          (1, 1) will keep the image aligned to the bottom
                          right
    :return: An image.
    """

    resized = contain(image, size, method)
    if resized.size == size:
        out = resized
    else:
        out = Image.new(image.mode, size, color)
        if resized.palette:
            palette = resized.getpalette()
            if palette is not None:
                out.putpalette(palette)
        if resized.width != size[0]:
            x = round((size[0] - resized.width) * max(0, min(centering[0], 1)))
            out.paste(resized, (x, 0))
        else:
            y = round((size[1] - resized.height) * max(0, min(centering[1], 1)))
            out.paste(resized, (0, y))
    return out


def pad(
    image: np.ndarray,
    padding: int | tuple[int, int] | Iterable[tuple[int, int]],
    mode: PaddingMode = PaddingMode.CONSTANT,
    constant_values: float | Iterable[float] = 0.0,
    data_format: str | ChannelDimension | None = None,
    input_data_format: str | ChannelDimension | None = None,
) -> np.ndarray:
    """
    Pads the `image` with the specified (height, width) `padding` and `mode`.

    Args:
        image (`np.ndarray`):
            The image to pad.
        padding (`int` or `tuple[int, int]` or `Iterable[tuple[int, int]]`):
            Padding to apply to the edges of the height, width axes. Can be one of three formats:
            - `((before_height, after_height), (before_width, after_width))` unique pad widths for each axis.
            - `((before, after),)` yields same before and after pad for height and width.
            - `(pad,)` or int is a shortcut for before = after = pad width for all axes.
        mode (`PaddingMode`):
            The padding mode to use. Can be one of:
                - `"constant"`: pads with a constant value.
                - `"reflect"`: pads with the reflection of the vector mirrored on the first and last values of the
                  vector along each axis.
                - `"replicate"`: pads with the replication of the last value on the edge of the array along each axis.
                - `"symmetric"`: pads with the reflection of the vector mirrored along the edge of the array.
        constant_values (`float` or `Iterable[float]`, *optional*):
            The value to use for the padding if `mode` is `"constant"`.
        data_format (`str` or `ChannelDimension`, *optional*):
            The channel dimension format for the output image. Can be one of:
                - `"channels_first"` or `ChannelDimension.FIRST`: image in (num_channels, height, width) format.
                - `"channels_last"` or `ChannelDimension.LAST`: image in (height, width, num_channels) format.
            If unset, will use same as the input image.
        input_data_format (`str` or `ChannelDimension`, *optional*):
            The channel dimension format for the input image. Can be one of:
                - `"channels_first"` or `ChannelDimension.FIRST`: image in (num_channels, height, width) format.
                - `"channels_last"` or `ChannelDimension.LAST`: image in (height, width, num_channels) format.
            If unset, will use the inferred format of the input image.

    Returns:
        `np.ndarray`: The padded image.

    """
    if input_data_format is None:
        input_data_format = infer_channel_dimension_format(image)

    def _expand_for_data_format(values):
        """
        Convert values to be in the format expected by np.pad based on the data format.
        """
        if isinstance(values, (int, float)):
            values = ((values, values), (values, values))
        elif isinstance(values, tuple) and len(values) == 1:
            values = ((values[0], values[0]), (values[0], values[0]))
        elif isinstance(values, tuple) and len(values) == 2 and isinstance(values[0], int):
            values = (values, values)
        elif isinstance(values, tuple) and len(values) == 2 and isinstance(values[0], tuple):
            pass
        else:
            raise ValueError(f"Unsupported format: {values}")

        # add 0 for channel dimension
        values = ((0, 0), *values) if input_data_format == ChannelDimension.FIRST else (*values, (0, 0))

        # Add additional padding if there's a batch dimension
        values = ((0, 0), *values) if image.ndim == 4 else values
        return values

    padding = _expand_for_data_format(padding)

    if mode == PaddingMode.CONSTANT:
        constant_values = _expand_for_data_format(constant_values)
        image = np.pad(image, padding, mode="constant", constant_values=constant_values)
    elif mode == PaddingMode.REFLECT:
        image = np.pad(image, padding, mode="reflect")
    elif mode == PaddingMode.REPLICATE:
        image = np.pad(image, padding, mode="edge")
    elif mode == PaddingMode.SYMMETRIC:
        image = np.pad(image, padding, mode="symmetric")
    else:
        raise ValueError(f"Invalid padding mode: {mode}")

    image = to_channel_dimension_format(image, data_format, input_data_format) if data_format is not None else image
    return image


def pad(
    video: np.ndarray,
    padding: int | tuple[int, int] | Iterable[tuple[int, int]],
    mode: PaddingMode = PaddingMode.CONSTANT,
    constant_values: float | Iterable[float] = 0.0,
    data_format: str | ChannelDimension | None = None,
    input_data_format: str | ChannelDimension | None = None,
) -> np.ndarray:
    """
    Pads the `video` with the specified (height, width) `padding` and `mode`.

    Args:
        video (`np.ndarray`):
            The video to pad.
        padding (`int` or `tuple[int, int]` or `Iterable[tuple[int, int]]`):
            Padding to apply to the edges of the height, width axes. Can be one of three formats:
            - `((before_height, after_height), (before_width, after_width))` unique pad widths for each axis.
            - `((before, after),)` yields same before and after pad for height and width.
            - `(pad,)` or int is a shortcut for before = after = pad width for all axes.
        mode (`PaddingMode`):
            The padding mode to use. Can be one of:
                - `"constant"`: pads with a constant value.
                - `"reflect"`: pads with the reflection of the vector mirrored on the first and last values of the
                  vector along each axis.
                - `"replicate"`: pads with the replication of the last value on the edge of the array along each axis.
                - `"symmetric"`: pads with the reflection of the vector mirrored along the edge of the array.
        constant_values (`float` or `Iterable[float]`, *optional*):
            The value to use for the padding if `mode` is `"constant"`.
        data_format (`str` or `ChannelDimension`, *optional*):
            The channel dimension format for the output video. Can be one of:
                - `"channels_first"` or `ChannelDimension.FIRST`: video in (num_frames, num_channels, height, width) format.
                - `"channels_last"` or `ChannelDimension.LAST`: video in (num_frames, height, width, num_channels) format.
            If unset, will use same as the input video.
        input_data_format (`str` or `ChannelDimension`, *optional*):
            The channel dimension format for the input video. Can be one of:
                - `"channels_first"` or `ChannelDimension.FIRST`: video in (num_frames, num_channels, height, width) format.
                - `"channels_last"` or `ChannelDimension.LAST`: video in (num_frames, height, width, num_channels) format.
            If unset, will use the inferred format of the input video.

    Returns:
        `np.ndarray`: The padded video.

    """
    if input_data_format is None:
        input_data_format = infer_channel_dimension_format(video)

    def _expand_for_data_format(values):
        """
        Convert values to be in the format expected by np.pad based on the data format.
        """
        if isinstance(values, (int, float)):
            values = ((values, values), (values, values))
        elif isinstance(values, tuple) and len(values) == 1:
            values = ((values[0], values[0]), (values[0], values[0]))
        elif isinstance(values, tuple) and len(values) == 2 and isinstance(values[0], int):
            values = (values, values)
        elif isinstance(values, tuple) and len(values) == 2 and isinstance(values[0], tuple):
            pass
        else:
            raise ValueError(f"Unsupported format: {values}")

        # add 0 for channel dimension
        values = (
            ((0, 0), (0, 0), *values) if input_data_format == ChannelDimension.FIRST else ((0, 0), *values, (0, 0))
        )

        # Add additional padding if there's a batch dimension
        values = (0, *values) if video.ndim == 5 else values
        return values

    padding_map = {
        PaddingMode.CONSTANT: "constant",
        PaddingMode.REFLECT: "reflect",
        PaddingMode.REPLICATE: "replicate",
        PaddingMode.SYMMETRIC: "symmetric",
    }
    padding = _expand_for_data_format(padding)

    pad_kwargs = {}
    if mode not in padding_map:
        raise ValueError(f"Invalid padding mode: {mode}")
    elif mode == PaddingMode.CONSTANT:
        pad_kwargs["constant_values"] = _expand_for_data_format(constant_values)

    video = np.pad(video, padding, mode=padding_map[mode], **pad_kwargs)
    video = to_channel_dimension_format(video, data_format, input_data_format) if data_format is not None else video
    return video


def pad(s: str, padding: int, offset: int = 0, char: str = " "):
    if padding >= len(s):
        padding -= len(s)
    return "".join([char for _ in range(padding + offset)]) + s


def pad(
    input: Tensor,
    pad: list[int],
    mode: str = "constant",
    value: float | None = None,
) -> Tensor:
    r"""
    pad(input, pad, mode="constant", value=None) -> Tensor

    Pads tensor.

    Padding size:
        The padding size by which to pad some dimensions of :attr:`input`
        are described starting from the last dimension and moving forward.
        :math:`\left\lfloor\frac{\text{len(pad)}}{2}\right\rfloor` dimensions
        of ``input`` will be padded.
        For example, to pad only the last dimension of the input tensor, then
        :attr:`pad` has the form
        :math:`(\text{padding\_left}, \text{padding\_right})`;
        to pad the last 2 dimensions of the input tensor, then use
        :math:`(\text{padding\_left}, \text{padding\_right},`
        :math:`\text{padding\_top}, \text{padding\_bottom})`;
        to pad the last 3 dimensions, use
        :math:`(\text{padding\_left}, \text{padding\_right},`
        :math:`\text{padding\_top}, \text{padding\_bottom}`
        :math:`\text{padding\_front}, \text{padding\_back})`.

    Padding mode:
        See :class:`torch.nn.CircularPad2d`, :class:`torch.nn.ConstantPad2d`,
        :class:`torch.nn.ReflectionPad2d`, and :class:`torch.nn.ReplicationPad2d`
        for concrete examples on how each of the padding modes works. Constant
        padding is implemented for arbitrary dimensions. Circular, replicate and
        reflection padding are implemented for padding the last 3 dimensions of a
        4D or 5D input tensor, the last 2 dimensions of a 3D or 4D input tensor,
        or the last dimension of a 2D or 3D input tensor.

    Note:
        When using the CUDA backend, this operation may induce nondeterministic
        behaviour in its backward pass that is not easily switched off.
        Please see the notes on :doc:`/notes/randomness` for background.

    Args:
        input (Tensor): N-dimensional tensor
        pad (tuple): m-elements tuple, where
            :math:`\frac{m}{2} \leq` input dimensions and :math:`m` is even.
        mode: ``'constant'``, ``'reflect'``, ``'replicate'`` or ``'circular'``.
            Default: ``'constant'``
        value: fill value for ``'constant'`` padding. Default: ``0``

    Examples::

        >>> t4d = torch.empty(3, 3, 4, 2)
        >>> p1d = (1, 1) # pad last dim by 1 on each side
        >>> out = F.pad(t4d, p1d, "constant", 0)  # effectively zero padding
        >>> print(out.size())
        torch.Size([3, 3, 4, 4])
        >>> p2d = (1, 1, 2, 2) # pad last dim by (1, 1) and 2nd to last by (2, 2)
        >>> out = F.pad(t4d, p2d, "constant", 0)
        >>> print(out.size())
        torch.Size([3, 3, 8, 4])
        >>> t4d = torch.empty(3, 3, 4, 2)
        >>> p3d = (0, 1, 2, 1, 3, 3) # pad by (0, 1), (2, 1), and (3, 3)
        >>> out = F.pad(t4d, p3d, "constant", 0)
        >>> print(out.size())
        torch.Size([3, 9, 7, 3])
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            torch.nn.functional.pad, (input,), input, pad, mode=mode, value=value
        )
    if not torch.jit.is_scripting():
        if torch.are_deterministic_algorithms_enabled() and (
            input.is_cuda or input.is_xpu
        ):
            if mode == "replicate":
                # Use slow decomp whose backward will be in terms of index_put.
                if torch.compiler.is_compiling():
                    # nonstrict_trace makes Dynamo skip the function body
                    # (which contains Dynamo-untraceable code) while
                    # AOTAutograd still traces into it for the backward.
                    return torch._dynamo.decorators.nonstrict_trace(
                        torch._decomp.decompositions._replication_pad
                    )(input, pad)
                # importlib is required because the import cannot be top level
                # (cycle) and cannot be nested (TS doesn't support)
                return importlib.import_module(
                    "torch._decomp.decompositions"
                )._replication_pad(input, pad)
    return torch._C._nn.pad(input, pad, mode, value)


def pad(array: ArrayLike, pad_width: ArrayLike, mode="constant", **kwargs):
    if mode != "constant":
        raise NotImplementedError
    value = kwargs.get("constant_values", 0)
    # `value` must be a python scalar for torch.nn.functional.pad
    typ = _dtypes_impl.python_type_for_torch(array.dtype)
    value = typ(value)

    pad_width = torch.broadcast_to(pad_width, (array.ndim, 2))
    pad_width = torch.flip(pad_width, (0,)).flatten()

    return torch.nn.functional.pad(array, tuple(pad_width), value=value)


def pad(
    g: jit_utils.GraphContext,
    input: _C.Value,
    pad: _C.Value,
    mode: _C.Value,
    value: _C.Value,
):
    mode = symbolic_helper._parse_arg(mode, "s")
    if mode == "replicate":
        return replication_pad(g, input, pad)
    elif mode == "reflect":
        return reflection_pad(g, input, pad)
    elif mode == "constant":
        return constant_pad_nd(g, input, pad, value)
    elif mode == "circular":
        return opset9._pad_circular(g, input, pad)
    else:
        raise errors.SymbolicValueError(f"Unrecognized padding mode {mode}", input)


def pad(
    g: jit_utils.GraphContext,
    input: _C.Value,
    pad: _C.Value,
    mode: _C.Value,
    value: _C.Value,
):
    mode = symbolic_helper._parse_arg(mode, "s")
    if mode == "replicate":
        return replication_pad(g, input, pad)
    elif mode == "reflect":
        return reflection_pad(g, input, pad)
    elif mode == "constant":
        return constant_pad_nd(g, input, pad, value)
    elif mode == "circular":
        return _pad_circular(g, input, pad)
    else:
        raise errors.SymbolicValueError(f"Unrecognized padding mode {mode}", input)


def pad(
    x: Array,
    pad_width: int | tuple[int, int] | Sequence[tuple[int, int]],
    mode: Literal["constant"] = "constant",
    *,
    constant_values: complex = 0,
    xp: ModuleType | None = None,
) -> Array:
    """
    Pad the input array.

    Parameters
    ----------
    x : array
        Input array.
    pad_width : int or tuple of ints or sequence of pairs of ints
        Pad the input array with this many elements from each side.
        If a sequence of tuples, ``[(before_0, after_0), ... (before_N, after_N)]``,
        each pair applies to the corresponding axis of ``x``.
        A single tuple, ``(before, after)``, is equivalent to a list of ``x.ndim``
        copies of this tuple.
    mode : str, optional
        Only "constant" mode is currently supported, which pads with
        the value passed to `constant_values`.
    constant_values : python scalar, optional
        Use this value to pad the input. Default is zero.
    xp : array_namespace, optional
        The standard-compatible namespace for `x`. Default: infer.

    Returns
    -------
    array
        The input array,
        padded with ``pad_width`` elements equal to ``constant_values``.
    """
    xp = array_namespace(x) if xp is None else xp

    if mode != "constant":
        msg = "Only `'constant'` mode is currently supported"
        raise NotImplementedError(msg)

    if (
        is_numpy_namespace(xp)
        or is_cupy_namespace(xp)
        or is_jax_namespace(xp)
        or is_pydata_sparse_namespace(xp)
    ):
        return xp.pad(x, pad_width, mode, constant_values=constant_values)

    # https://github.com/pytorch/pytorch/blob/cf76c05b4dc629ac989d1fb8e789d4fac04a095a/torch/_numpy/_funcs_impl.py#L2045-L2056
    if is_torch_namespace(xp):
        pad_width = xp.asarray(pad_width)
        pad_width = xp.broadcast_to(pad_width, (x.ndim, 2))
        pad_width = xp.flip(pad_width, axis=(0,)).flatten()
        return xp.nn.functional.pad(x, tuple(pad_width), value=constant_values)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]

    return _funcs.pad(x, pad_width, constant_values=constant_values, xp=xp)


def pad(
    x: Array,
    pad_width: int | tuple[int, int] | Sequence[tuple[int, int]],
    *,
    constant_values: complex = 0,
    xp: ModuleType,
) -> Array:  # numpydoc ignore=PR01,RT01
    """See docstring in `array_api_extra._delegation.py`."""
    # make pad_width a list of length-2 tuples of ints
    if isinstance(pad_width, int):
        pad_width_seq = [(pad_width, pad_width)] * x.ndim
    elif (
        isinstance(pad_width, tuple)
        and len(pad_width) == 2
        and all(isinstance(i, int) for i in pad_width)
    ):
        pad_width_seq = [cast(tuple[int, int], pad_width)] * x.ndim
    else:
        pad_width_seq = cast(list[tuple[int, int]], list(pad_width))

    slices: list[slice] = []
    newshape: list[int] = []
    for ax, w_tpl in enumerate(pad_width_seq):
        if len(w_tpl) != 2:
            msg = f"expect a 2-tuple (before, after), got {w_tpl}."
            raise ValueError(msg)

        sh = eager_shape(x)[ax]

        if w_tpl[0] == 0 and w_tpl[1] == 0:
            sl = slice(None, None, None)
        else:
            stop: int | None
            start, stop = w_tpl
            stop = None if stop == 0 else -stop

            sl = slice(start, stop, None)
            sh += w_tpl[0] + w_tpl[1]

        newshape.append(sh)
        slices.append(sl)

    padded = xp.full(
        tuple(newshape),
        fill_value=constant_values,
        dtype=x.dtype,
        device=_compat.device(x),
    )
    return at(padded, tuple(slices)).set(x)


def pad(array, pad_width, mode='constant', **kwargs):
    """
    Pad an array.

    Parameters
    ----------
    array : array_like of rank N
        The array to pad.
    pad_width : {sequence, array_like, int, dict}
        Number of values padded to the edges of each axis.
        ``((before_1, after_1), ... (before_N, after_N))`` unique pad widths
        for each axis.
        ``(before, after)`` or ``((before, after),)`` yields same before
        and after pad for each axis.
        ``(pad,)`` or ``int`` is a shortcut for before = after = pad width
        for all axes.
        If a ``dict``, each key is an axis and its corresponding value is an ``int`` or
        ``int`` pair describing the padding ``(before, after)`` or ``pad`` width for
        that axis.
    mode : str or function, optional
        One of the following string values or a user supplied function.

        'constant' (default)
            Pads with a constant value.
        'edge'
            Pads with the edge values of array.
        'linear_ramp'
            Pads with the linear ramp between end_value and the
            array edge value.
        'maximum'
            Pads with the maximum value of all or part of the
            vector along each axis.
        'mean'
            Pads with the mean value of all or part of the
            vector along each axis.
        'median'
            Pads with the median value of all or part of the
            vector along each axis.
        'minimum'
            Pads with the minimum value of all or part of the
            vector along each axis.
        'reflect'
            Pads with the reflection of the vector mirrored on
            the first and last values of the vector along each
            axis.
        'symmetric'
            Pads with the reflection of the vector mirrored
            along the edge of the array.
        'wrap'
            Pads with the wrap of the vector along the axis.
            The first values are used to pad the end and the
            end values are used to pad the beginning.
        'empty'
            Pads with undefined values.

        <function>
            Padding function, see Notes.
    stat_length : sequence or int, optional
        Used in 'maximum', 'mean', 'median', and 'minimum'.  Number of
        values at edge of each axis used to calculate the statistic value.

        ``((before_1, after_1), ... (before_N, after_N))`` unique statistic
        lengths for each axis.

        ``(before, after)`` or ``((before, after),)`` yields same before
        and after statistic lengths for each axis.

        ``(stat_length,)`` or ``int`` is a shortcut for
        ``before = after = statistic`` length for all axes.

        Default is ``None``, to use the entire axis.
    constant_values : sequence or scalar, optional
        Used in 'constant'.  The values to set the padded values for each
        axis.

        ``((before_1, after_1), ... (before_N, after_N))`` unique pad constants
        for each axis.

        ``(before, after)`` or ``((before, after),)`` yields same before
        and after constants for each axis.

        ``(constant,)`` or ``constant`` is a shortcut for
        ``before = after = constant`` for all axes.

        Default is 0.
    end_values : sequence or scalar, optional
        Used in 'linear_ramp'.  The values used for the ending value of the
        linear_ramp and that will form the edge of the padded array.

        ``((before_1, after_1), ... (before_N, after_N))`` unique end values
        for each axis.

        ``(before, after)`` or ``((before, after),)`` yields same before
        and after end values for each axis.

        ``(constant,)`` or ``constant`` is a shortcut for
        ``before = after = constant`` for all axes.

        Default is 0.
    reflect_type : {'even', 'odd'}, optional
        Used in 'reflect', and 'symmetric'.  The 'even' style is the
        default with an unaltered reflection around the edge value.  For
        the 'odd' style, the extended part of the array is created by
        subtracting the reflected values from two times the edge value.

    Returns
    -------
    pad : ndarray
        Padded array of rank equal to `array` with shape increased
        according to `pad_width`.

    Notes
    -----
    For an array with rank greater than 1, some of the padding of later
    axes is calculated from padding of previous axes.  This is easiest to
    think about with a rank 2 array where the corners of the padded array
    are calculated by using padded values from the first axis.

    The padding function, if used, should modify a rank 1 array in-place. It
    has the following signature::

        padding_func(vector, iaxis_pad_width, iaxis, kwargs)

    where

    vector : ndarray
        A rank 1 array already padded with zeros.  Padded values are
        vector[:iaxis_pad_width[0]] and vector[-iaxis_pad_width[1]:].
    iaxis_pad_width : tuple
        A 2-tuple of ints, iaxis_pad_width[0] represents the number of
        values padded at the beginning of vector where
        iaxis_pad_width[1] represents the number of values padded at
        the end of vector.
    iaxis : int
        The axis currently being calculated.
    kwargs : dict
        Any keyword arguments the function requires.

    Examples
    --------
    >>> import numpy as np
    >>> a = [1, 2, 3, 4, 5]
    >>> np.pad(a, (2, 3), 'constant', constant_values=(4, 6))
    array([4, 4, 1, ..., 6, 6, 6])

    >>> np.pad(a, (2, 3), 'edge')
    array([1, 1, 1, ..., 5, 5, 5])

    >>> np.pad(a, (2, 3), 'linear_ramp', end_values=(5, -4))
    array([ 5,  3,  1,  2,  3,  4,  5,  2, -1, -4])

    >>> np.pad(a, (2,), 'maximum')
    array([5, 5, 1, 2, 3, 4, 5, 5, 5])

    >>> np.pad(a, (2,), 'mean')
    array([3, 3, 1, 2, 3, 4, 5, 3, 3])

    >>> np.pad(a, (2,), 'median')
    array([3, 3, 1, 2, 3, 4, 5, 3, 3])

    >>> a = [[1, 2], [3, 4]]
    >>> np.pad(a, ((3, 2), (2, 3)), 'minimum')
    array([[1, 1, 1, 2, 1, 1, 1],
           [1, 1, 1, 2, 1, 1, 1],
           [1, 1, 1, 2, 1, 1, 1],
           [1, 1, 1, 2, 1, 1, 1],
           [3, 3, 3, 4, 3, 3, 3],
           [1, 1, 1, 2, 1, 1, 1],
           [1, 1, 1, 2, 1, 1, 1]])

    >>> a = [1, 2, 3, 4, 5]
    >>> np.pad(a, (2, 3), 'reflect')
    array([3, 2, 1, 2, 3, 4, 5, 4, 3, 2])

    >>> np.pad(a, (2, 3), 'reflect', reflect_type='odd')
    array([-1,  0,  1,  2,  3,  4,  5,  6,  7,  8])

    >>> np.pad(a, (2, 3), 'symmetric')
    array([2, 1, 1, 2, 3, 4, 5, 5, 4, 3])

    >>> np.pad(a, (2, 3), 'symmetric', reflect_type='odd')
    array([0, 1, 1, 2, 3, 4, 5, 5, 6, 7])

    >>> np.pad(a, (2, 3), 'wrap')
    array([4, 5, 1, 2, 3, 4, 5, 1, 2, 3])

    >>> def pad_with(vector, pad_width, iaxis, kwargs):
    ...     pad_value = kwargs.get('padder', 10)
    ...     vector[:pad_width[0]] = pad_value
    ...     vector[-pad_width[1]:] = pad_value
    >>> a = np.arange(6)
    >>> a = a.reshape((2, 3))
    >>> np.pad(a, 2, pad_with)
    array([[10, 10, 10, 10, 10, 10, 10],
           [10, 10, 10, 10, 10, 10, 10],
           [10, 10,  0,  1,  2, 10, 10],
           [10, 10,  3,  4,  5, 10, 10],
           [10, 10, 10, 10, 10, 10, 10],
           [10, 10, 10, 10, 10, 10, 10]])
    >>> np.pad(a, 2, pad_with, padder=100)
    array([[100, 100, 100, 100, 100, 100, 100],
           [100, 100, 100, 100, 100, 100, 100],
           [100, 100,   0,   1,   2, 100, 100],
           [100, 100,   3,   4,   5, 100, 100],
           [100, 100, 100, 100, 100, 100, 100],
           [100, 100, 100, 100, 100, 100, 100]])

    >>> a = np.arange(1, 7).reshape(2, 3)
    >>> np.pad(a, {1: (1, 2)})
    array([[0, 1, 2, 3, 0, 0],
           [0, 4, 5, 6, 0, 0]])
    >>> np.pad(a, {-1: 2})
    array([[0, 0, 1, 2, 3, 0, 0],
           [0, 0, 4, 5, 6, 0, 0]])
    >>> np.pad(a, {0: (3, 0)})
    array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0],
           [1, 2, 3],
           [4, 5, 6]])
    >>> np.pad(a, {0: (3, 0), 1: 2})
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 2, 3, 0, 0],
           [0, 0, 4, 5, 6, 0, 0]])
    """
    array = np.asarray(array)
    if isinstance(pad_width, dict):
        seq = [(0, 0)] * array.ndim
        for axis, width in pad_width.items():
            match width:
                case int(both):
                    seq[axis] = both, both
                case tuple((int(before), int(after))):
                    seq[axis] = before, after
                case _ as invalid:
                    typing.assert_never(invalid)
        pad_width = seq
    pad_width = np.asarray(pad_width)

    if not pad_width.dtype.kind == 'i':
        raise TypeError('`pad_width` must be of integral type.')

    # Broadcast to shape (array.ndim, 2)
    pad_width = _as_pairs(pad_width, array.ndim, as_index=True)

    if callable(mode):
        # Old behavior: Use user-supplied function with np.apply_along_axis
        function = mode
        # Create a new zero padded array
        padded, _ = _pad_simple(array, pad_width, fill_value=0)
        # And apply along each axis

        for axis in range(padded.ndim):
            # Iterate using ndindex as in apply_along_axis, but assuming that
            # function operates inplace on the padded array.

            # view with the iteration axis at the end
            view = np.moveaxis(padded, axis, -1)

            # compute indices for the iteration axes, and append a trailing
            # ellipsis to prevent 0d arrays decaying to scalars (gh-8642)
            inds = ndindex(view.shape[:-1])
            inds = (ind + (Ellipsis,) for ind in inds)
            for ind in inds:
                function(view[ind], pad_width[axis], axis, kwargs)

        return padded

    # Make sure that no unsupported keywords were passed for the current mode
    allowed_kwargs = {
        'empty': [], 'edge': [], 'wrap': [],
        'constant': ['constant_values'],
        'linear_ramp': ['end_values'],
        'maximum': ['stat_length'],
        'mean': ['stat_length'],
        'median': ['stat_length'],
        'minimum': ['stat_length'],
        'reflect': ['reflect_type'],
        'symmetric': ['reflect_type'],
    }
    try:
        unsupported_kwargs = set(kwargs) - set(allowed_kwargs[mode])
    except KeyError:
        raise ValueError(f"mode '{mode}' is not supported") from None
    if unsupported_kwargs:
        raise ValueError("unsupported keyword arguments for mode "
                         f"'{mode}': {unsupported_kwargs}")

    stat_functions = {"maximum": np.amax, "minimum": np.amin,
                      "mean": np.mean, "median": np.median}

    # Create array with final shape and original values
    # (padded area is undefined)
    padded, original_area_slice = _pad_simple(array, pad_width)
    # And prepare iteration over all dimensions
    # (zipping may be more readable than using enumerate)
    axes = range(padded.ndim)

    if mode == "constant":
        values = kwargs.get("constant_values", 0)
        values = _as_pairs(values, padded.ndim)
        for axis, width_pair, value_pair in zip(axes, pad_width, values):
            roi = _view_roi(padded, original_area_slice, axis)
            _set_pad_area(roi, axis, width_pair, value_pair)

    elif mode == "empty":
        pass  # Do nothing as _pad_simple already returned the correct result

    elif array.size == 0:
        # Only modes "constant" and "empty" can extend empty axes, all other
        # modes depend on `array` not being empty
        # -> ensure every empty axis is only "padded with 0"
        for axis, width_pair in zip(axes, pad_width):
            if array.shape[axis] == 0 and any(width_pair):
                raise ValueError(
                    f"can't extend empty axis {axis} using modes other than "
                    "'constant' or 'empty'"
                )
        # passed, don't need to do anything more as _pad_simple already
        # returned the correct result

    elif mode == "edge":
        for axis, width_pair in zip(axes, pad_width):
            roi = _view_roi(padded, original_area_slice, axis)
            edge_pair = _get_edges(roi, axis, width_pair)
            _set_pad_area(roi, axis, width_pair, edge_pair)

    elif mode == "linear_ramp":
        end_values = kwargs.get("end_values", 0)
        end_values = _as_pairs(end_values, padded.ndim)
        for axis, width_pair, value_pair in zip(axes, pad_width, end_values):
            roi = _view_roi(padded, original_area_slice, axis)
            ramp_pair = _get_linear_ramps(roi, axis, width_pair, value_pair)
            _set_pad_area(roi, axis, width_pair, ramp_pair)

    elif mode in stat_functions:
        func = stat_functions[mode]
        length = kwargs.get("stat_length")
        length = _as_pairs(length, padded.ndim, as_index=True)
        for axis, width_pair, length_pair in zip(axes, pad_width, length):
            roi = _view_roi(padded, original_area_slice, axis)
            stat_pair = _get_stats(roi, axis, width_pair, length_pair, func)
            _set_pad_area(roi, axis, width_pair, stat_pair)

    elif mode in {"reflect", "symmetric"}:
        method = kwargs.get("reflect_type", "even")
        include_edge = mode == "symmetric"
        for axis, (left_index, right_index) in zip(axes, pad_width):
            if array.shape[axis] == 1 and (left_index > 0 or right_index > 0):
                # Extending singleton dimension for 'reflect' is legacy
                # behavior; it really should raise an error.
                edge_pair = _get_edges(padded, axis, (left_index, right_index))
                _set_pad_area(
                    padded, axis, (left_index, right_index), edge_pair)
                continue

            roi = _view_roi(padded, original_area_slice, axis)
            while left_index > 0 or right_index > 0:
                # Iteratively pad until dimension is filled with reflected
                # values. This is necessary if the pad area is larger than
                # the length of the original values in the current dimension.
                left_index, right_index = _set_reflect_both(
                    roi, axis, (left_index, right_index),
                    method, array.shape[axis], include_edge
                )

    elif mode == "wrap":
        for axis, (left_index, right_index) in zip(axes, pad_width):
            roi = _view_roi(padded, original_area_slice, axis)
            original_period = padded.shape[axis] - right_index - left_index
            while left_index > 0 or right_index > 0:
                # Iteratively pad until dimension is filled with wrapped
                # values. This is necessary if the pad area is larger than
                # the length of the original values in the current dimension.
                left_index, right_index = _set_wrap_both(
                    roi, axis, (left_index, right_index), original_period)

    return padded


def pad(operand: _ods_ir.Value[_ods_ir.RankedTensorType], padding_value: _ods_ir.Value[_ods_ir.RankedTensorType], edge_padding_low: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], edge_padding_high: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], interior_padding: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return PadOp(operand=operand, padding_value=padding_value, edge_padding_low=edge_padding_low, edge_padding_high=edge_padding_high, interior_padding=interior_padding, results=results, loc=loc, ip=ip).result


def pad(operand: _ods_ir.Value[_ods_ir.RankedTensorType], padding_value: _ods_ir.Value[_ods_ir.RankedTensorType], edge_padding_low: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], edge_padding_high: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], interior_padding: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return PadOp(operand=operand, padding_value=padding_value, edge_padding_low=edge_padding_low, edge_padding_high=edge_padding_high, interior_padding=interior_padding, results=results, loc=loc, ip=ip).result


def pad(operand, padding_value, padding_config):
  # https://www.openxla.org/xla/operation_semantics#pad
  lo, hi, interior = util.unzip3(padding_config)
  # Handle first the positive edge padding and interior
  lo_pos, hi_pos = np.clip(lo, 0, None), np.clip(hi, 0, None)
  outshape = np.add(np.add(np.add(lo_pos, hi_pos), operand.shape),
                     np.multiply(interior, np.subtract(operand.shape, 1)))
  out = np.full(outshape, padding_value, operand.dtype)
  lhs_slices = tuple(_slice(l if l > 0 else 0, -h if h > 0 else None, step)
                     for l, h, step in zip(lo_pos, hi_pos, np.add(1, interior)))
  out[lhs_slices] = operand
  trim_slices = tuple(_slice(-l if l < 0 else 0, h if h < 0 else None)
                     for l, h in zip(lo, hi))
  return out[trim_slices]


def pad(ctx: LoweringRuleContext, aval_out,
        x, padding_value,
        padding_low, padding_high, padding_interior) -> ir.Value:
  if all(core.is_constant_shape(s) for s in (padding_low,
                                             padding_high, padding_interior)):
    return hlo.pad(x, padding_value,
                   dense_int_array(padding_low),
                   dense_int_array(padding_high),
                   dense_int_array(padding_interior))
  else:
    padding_low = eval_dynamic_shape_as_tensor(ctx, padding_low)
    padding_high = eval_dynamic_shape_as_tensor(ctx, padding_high)
    padding_interior = eval_dynamic_shape_as_tensor(ctx, padding_interior)
    (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
    return hlo.dynamic_pad(
        result_type,
        x, padding_value, padding_low, padding_high, padding_interior)


def pad(operand: ArrayLike, padding_value: ArrayLike,
        padding_config: Sequence[tuple[int, int, int]]) -> Array:
  """Applies low, high, and/or interior padding to an array.

  Wraps XLA's `Pad
  <https://www.openxla.org/xla/operation_semantics#pad>`_
  operator.

  Args:
    operand: an array to be padded.
    padding_value: the value to be inserted as padding. Must have the same dtype
      as ``operand``.
    padding_config: a sequence of ``(low, high, interior)`` tuples of integers,
      giving the amount of low, high, and interior (dilation) padding to insert
      in each dimension. Negative values for ``low`` and ``high`` are allowed
      and remove elements from the edges of the array.

  Returns:
    The ``operand`` array with padding value ``padding_value`` inserted in each
    dimension according to the ``padding_config``.

  Examples:
    >>> from jax import lax
    >>> import jax.numpy as jnp

    Pad a 1-dimensional array with zeros, We'll specify two zeros in front and
    three at the end:

    >>> x = jnp.array([1, 2, 3, 4])
    >>> lax.pad(x, 0, [(2, 3, 0)])
    Array([0, 0, 1, 2, 3, 4, 0, 0, 0], dtype=int32)

    Pad a 1-dimensional array with *interior* zeros; i.e. insert a single zero
    between each value:

    >>> lax.pad(x, 0, [(0, 0, 1)])
    Array([1, 0, 2, 0, 3, 0, 4], dtype=int32)

    Pad a 2-dimensional array with the value ``-1`` at front and end, with a pad
    size of 2 in each dimension:

    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> lax.pad(x, -1, [(2, 2, 0), (2, 2, 0)])
    Array([[-1, -1, -1, -1, -1, -1, -1],
           [-1, -1, -1, -1, -1, -1, -1],
           [-1, -1,  1,  2,  3, -1, -1],
           [-1, -1,  4,  5,  6, -1, -1],
           [-1, -1, -1, -1, -1, -1, -1],
           [-1, -1, -1, -1, -1, -1, -1]], dtype=int32)

    Use negative padding to remove elements from the edges of an array:

    >>> x = jnp.array([1, 2, 3, 4, 5], dtype=jnp.int32)
    >>> lax.pad(x, 0, [(-1, -2, 0)])
    Array([2, 3], dtype=int32)
  """
  operand, padding_value = core.auto_insert_reshard(operand, padding_value)
  return pad_p.bind(operand, padding_value, padding_config=tuple(padding_config))


def pad(array: ArrayLike, pad_width: PadValueLike[int | Array | np.ndarray],
        mode: str | Callable[..., Any] = "constant", **kwargs) -> Array:
  """Add padding to an array.

  JAX implementation of :func:`numpy.pad`.

  Args:
    array: array to pad.
    pad_width: specify the pad width for each dimension of an array. Padding widths
      may be separately specified for *before* and *after* the array. Options are:

      - ``int`` or ``(int,)``: pad each array dimension with the same number of values
        both before and after.
      - ``(before, after)``: pad each array with ``before`` elements before, and ``after``
        elements after
      - ``((before_1, after_1), (before_2, after_2), ... (before_N, after_N))``: specify
        distinct ``before`` and ``after`` values for each array dimension.

    mode: a string or callable. Supported pad modes are:

      - ``'constant'`` (default): pad with a constant value, which defaults to zero.
      - ``'empty'``: pad with empty values (i.e. zero)
      - ``'edge'``: pad with the edge values of the array.
      - ``'wrap'``: pad by wrapping the array.
      - ``'linear_ramp'``: pad with a linear ramp to specified ``end_values``.
      - ``'maximum'``: pad with the maximum value.
      - ``'mean'``: pad with the mean value.
      - ``'median'``: pad with the median value.
      - ``'minimum'``: pad with the minimum value.
      - ``'reflect'``: pad by reflection.
      - ``'symmetric'``: pad by symmetric reflection.
      - ``<callable>``: a callable function. See Notes below.

    constant_values: referenced for ``mode = 'constant'``. Specify the constant value
      to pad with.
    stat_length: referenced for ``mode in ['maximum', 'mean', 'median', 'minimum']``.
      An integer or tuple specifying the number of edge values to use when calculating
      the statistic.
    end_values: referenced for ``mode = 'linear_ramp'``. Specify the end values to
      ramp the padding values to.
    reflect_type: referenced for ``mode in ['reflect', 'symmetric']``. Specify whether
      to use even or odd reflection.

  Returns:
    A padded copy of ``array``.

  Notes:
    When ``mode`` is callable, it should have the following signature::

      def pad_func(row: Array, pad_width: tuple[int, int],
                   iaxis: int, kwargs: dict) -> Array:
        ...

    Here ``row`` is a 1D slice of the padded array along axis ``iaxis``, with the pad
    values filled with zeros. ``pad_width`` is a tuple specifying the ``(before, after)``
    padding sizes, and ``kwargs`` are any additional keyword arguments passed to the
    :func:`jax.numpy.pad` function.

    Note that while in NumPy, the function should modify ``row`` in-place, in JAX the
    function should return the modified ``row``. In JAX, the custom padding function
    will be mapped across the padded axis using the :func:`jax.vmap` transformation.

  See also:
    - :func:`jax.numpy.resize`: resize an array
    - :func:`jax.numpy.tile`: create a larger array by tiling a smaller array.
    - :func:`jax.numpy.repeat`: create a larger array by repeating values of a smaller array.

  Examples:

    Pad a 1-dimensional array with zeros:

    >>> x = jnp.array([10, 20, 30, 40])
    >>> jnp.pad(x, 2)
    Array([ 0,  0, 10, 20, 30, 40,  0,  0], dtype=int32)
    >>> jnp.pad(x, (2, 4))
    Array([ 0,  0, 10, 20, 30, 40,  0,  0,  0,  0], dtype=int32)

    Pad a 1-dimensional array with specified values:

    >>> jnp.pad(x, 2, constant_values=99)
    Array([99, 99, 10, 20, 30, 40, 99, 99], dtype=int32)

    Pad a 1-dimensional array with the mean array value:

    >>> jnp.pad(x, 2, mode='mean')
    Array([25, 25, 10, 20, 30, 40, 25, 25], dtype=int32)

    Pad a 1-dimensional array with reflected values:

    >>> jnp.pad(x, 2, mode='reflect')
    Array([30, 20, 10, 20, 30, 40, 30, 20], dtype=int32)

    Pad a 2-dimensional array with different paddings in each dimension:

    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.pad(x, ((1, 2), (3, 0)))
    Array([[0, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 2, 3],
           [0, 0, 0, 4, 5, 6],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0]], dtype=int32)

    Pad a 1-dimensional array with a custom padding function:

    >>> def custom_pad(row, pad_width, iaxis, kwargs):
    ...   # row represents a 1D slice of the zero-padded array.
    ...   before, after = pad_width
    ...   before_value = kwargs.get('before_value', 0)
    ...   after_value = kwargs.get('after_value', 0)
    ...   row = row.at[:before].set(before_value)
    ...   return row.at[len(row) - after:].set(after_value)
    >>> x = jnp.array([2, 3, 4])
    >>> jnp.pad(x, 2, custom_pad, before_value=-10, after_value=10)
    Array([-10, -10,   2,   3,   4,  10,  10], dtype=int32)
  """

  array = util.ensure_arraylike("pad", array)
  pad_width = _broadcast_to_pairs(pad_width, np.ndim(array), "pad_width")
  if pad_width and not all(core.is_dim(p[0]) and core.is_dim(p[1])
                           for p in pad_width):
    raise TypeError('`pad_width` must be of integral type.')

  if callable(mode):
    return _pad_func(asarray(array), pad_width, mode, **kwargs)

  allowed_kwargs = {
      'empty': [], 'edge': [], 'wrap': [],
      'constant': ['constant_values'],
      'linear_ramp': ['end_values'],
      'maximum': ['stat_length'],
      'mean': ['stat_length'],
      'median': ['stat_length'],
      'minimum': ['stat_length'],
      'reflect': ['reflect_type'],
      'symmetric': ['reflect_type'],
  }
  try:
    unsupported_kwargs = set(kwargs) - set(allowed_kwargs[mode])
  except KeyError:
    msg = "Unimplemented padding mode '{}' for np.pad."
    raise NotImplementedError(msg.format(mode))
  if unsupported_kwargs:
    raise ValueError("unsupported keyword arguments for mode '{}': {}"
                     .format(mode, unsupported_kwargs))
  # Set default value if not given.
  constant_values = kwargs.get('constant_values', 0)
  stat_length = kwargs.get('stat_length', None)
  end_values = kwargs.get('end_values', 0)
  reflect_type = kwargs.get('reflect_type', "even")

  return _pad(array, pad_width, mode, constant_values, stat_length, end_values, reflect_type)


def pad(data, size):
    r"""Pad byte string 'data' with null bytes until its length is a
    multiple of 'size'.

    >>> len(pad(b'abcd', 4))
    4
    >>> len(pad(b'abcde', 2))
    6
    >>> len(pad(b'abcde', 4))
    8
    >>> pad(b'abcdef', 4) == b'abcdef\x00\x00'
    True
    """
    data = tobytes(data)
    if size > 1:
        remainder = len(data) % size
        if remainder:
            data += b"\0" * (size - remainder)
    return data

