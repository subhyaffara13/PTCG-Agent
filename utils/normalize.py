import re
from typing import Any, Optional, Tuple

def normalize(text):
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    text = re.sub(r"[^a-z0-9']+", " ", text.lower())
    return text.strip()


def normalize(text):
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    text = re.sub(r"[^a-z0-9']+", " ", text.lower())
    return text.strip()


def normalize(uri):
    return urlparse.urlsplit(uri).geturl()


def normalize(
    nbdict: Any,
    version: Optional[int] = None,
    version_minor: Optional[int] = None,
    *,
    relax_add_props: bool = False,
    strip_invalid_metadata: bool = False,
) -> tuple[int, Any]:
    """
    Normalise a notebook prior to validation.

    This tries to implement a couple of normalisation steps to standardise
    notebooks and make validation easier.

    You should in general not rely on this function and make sure the notebooks
    that reach nbformat are already in a normal form. If not you likely have a bug,
    and may have security issues.

    Parameters
    ----------
    nbdict : dict
        notebook document
    version : int
    version_minor : int
    relax_add_props : bool
        Whether to allow extra property in the Json schema validating the
        notebook.
    strip_invalid_metadata : bool
        Whether to strip metadata that does not exist in the Json schema when
        validating the notebook.

    Returns
    -------
    changes : int
        number of changes in the notebooks
    notebook : dict
        deep-copy of the original object with relevant changes.

    """
    nbdict = deepcopy(nbdict)
    nbdict_version, nbdict_version_minor = get_version(nbdict)
    if version is None:
        version = nbdict_version
    if version_minor is None:
        version_minor = nbdict_version_minor
    return _normalize(
        nbdict,
        version,
        version_minor,
        True,
        relax_add_props=relax_add_props,
        strip_invalid_metadata=strip_invalid_metadata,
    )


def normalize(
    type: AnyStr | None,
    namespace: AnyStr | None,
    name: AnyStr | None,
    version: AnyStr | None,
    qualifiers: AnyStr | dict[str, str] | None,
    subpath: AnyStr | None,
    encode: Literal[True] = ...,
) -> tuple[str, str | None, str, str | None, str | None, str | None]: ...


def normalize(
    type: AnyStr | None,
    namespace: AnyStr | None,
    name: AnyStr | None,
    version: AnyStr | None,
    qualifiers: AnyStr | dict[str, str] | None,
    subpath: AnyStr | None,
    encode: Literal[False] | None,
) -> tuple[str, str | None, str, str | None, dict[str, str], str | None]: ...


def normalize(
    type: AnyStr | None,
    namespace: AnyStr | None,
    name: AnyStr | None,
    version: AnyStr | None,
    qualifiers: AnyStr | dict[str, str] | None,
    subpath: AnyStr | None,
    encode: bool | None = ...,
) -> tuple[str, str | None, str, str | None, str | dict[str, str] | None, str | None]: ...


def normalize(
    type: AnyStr | None,
    namespace: AnyStr | None,
    name: AnyStr | None,
    version: AnyStr | None,
    qualifiers: AnyStr | dict[str, str] | None,
    subpath: AnyStr | None,
    encode: bool | None = True,
) -> tuple[
    str | None,
    str | None,
    str | None,
    str | None,
    str | dict[str, str] | None,
    str | None,
]:
    """
    Return normalized purl components
    """
    type_norm = normalize_type(type, encode)
    namespace_norm = normalize_namespace(namespace, type_norm, encode)
    name_norm = normalize_name(name, qualifiers, type_norm, encode)
    version_norm = normalize_version(version, type, encode)
    qualifiers_norm = normalize_qualifiers(qualifiers, encode)
    subpath_norm = normalize_subpath(subpath, encode)
    return type_norm, namespace_norm, name_norm, version_norm, qualifiers_norm, subpath_norm


def normalize(
    image: np.ndarray,
    mean: float | Collection[float],
    std: float | Collection[float],
    data_format: ChannelDimension | None = None,
    input_data_format: str | ChannelDimension | None = None,
) -> np.ndarray:
    """
    Normalizes `image` using the mean and standard deviation specified by `mean` and `std`.

    image = (image - mean) / std

    Args:
        image (`np.ndarray`):
            The image to normalize.
        mean (`float` or `Collection[float]`):
            The mean to use for normalization.
        std (`float` or `Collection[float]`):
            The standard deviation to use for normalization.
        data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the output image. If unset, will use the inferred format from the input.
        input_data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the input image. If unset, will use the inferred format from the input.
    """
    if not isinstance(image, np.ndarray):
        raise TypeError("image must be a numpy array")

    if input_data_format is None:
        input_data_format = infer_channel_dimension_format(image)

    channel_axis = get_channel_dimension_axis(image, input_data_format=input_data_format)
    num_channels = image.shape[channel_axis]

    # We cast to float32 to avoid errors that can occur when subtracting uint8 values.
    # We preserve the original dtype if it is a float type to prevent upcasting float16.
    if not np.issubdtype(image.dtype, np.floating):
        image = image.astype(np.float32)

    if isinstance(mean, Collection):
        if len(mean) != num_channels:
            raise ValueError(f"mean must have {num_channels} elements if it is an iterable, got {len(mean)}")
    else:
        mean = [mean] * num_channels
    mean = np.array(mean, dtype=image.dtype)

    if isinstance(std, Collection):
        if len(std) != num_channels:
            raise ValueError(f"std must have {num_channels} elements if it is an iterable, got {len(std)}")
    else:
        std = [std] * num_channels
    std = np.array(std, dtype=image.dtype)

    if input_data_format == ChannelDimension.LAST:
        image = (image - mean) / std
    else:
        image = ((image.T - mean) / std).T

    image = to_channel_dimension_format(image, data_format, input_data_format) if data_format is not None else image
    return image


def normalize(input_tensors):
    if isinstance(input_tensors, list):
        out = []
        for tensor in input_tensors:
            out.append(nn.functional.normalize(tensor, p=2, dim=-1))
        return out
    else:
        return nn.functional.normalize(input_tensors, p=2, dim=-1)


def normalize(
    input: Tensor | MaskedTensor,
    ord: float,
    dim: int,
    *,
    eps: float = 1e-12,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    if dtype is None:
        dtype = input.dtype
    # TODO: eliminate mask_input as unnecessary when using masked divide.
    mask_input = _combine_input_and_mask(sum, input, mask)
    if mask_input.layout == torch.strided:
        nrm_ = norm(input, ord, dim, keepdim=True, dtype=dtype, mask=mask)
        # TODO: replace torch.maximum with masked maximum when available.
        denom = torch.maximum(nrm_, nrm_.new_full([], eps))
        # TODO: replace torch.divide with masked divide when available.
        return torch.divide(mask_input, denom)
    else:
        raise ValueError(
            f"masked normalize expects strided tensor (got {mask_input.layout} tensor)"
        )


def normalize(
    input: Tensor,
    p: float = 2.0,
    dim: int = 1,
    eps: float = 1e-12,
    out: Tensor | None = None,
) -> Tensor:
    r"""Perform :math:`L_p` normalization of inputs over specified dimension.

    For a tensor :attr:`input` of sizes :math:`(n_0, ..., n_{dim}, ..., n_k)`, each
    :math:`n_{dim}` -element vector :math:`v` along dimension :attr:`dim` is transformed as

    .. math::
        v = \frac{v}{\max(\lVert v \rVert_p, \epsilon)}.

    With the default arguments it uses the Euclidean norm over vectors along dimension :math:`1` for normalization.

    Args:
        input: input tensor of any shape
        p (float): the exponent value in the norm formulation. Default: 2
        dim (int or tuple of ints): the dimension to reduce. Default: 1
        eps (float): small value to avoid division by zero. Default: 1e-12
        out (Tensor, optional): the output tensor. If :attr:`out` is used, this
                                operation won't be differentiable.
    """
    if has_torch_function_variadic(input, out):
        return handle_torch_function(
            normalize, (input, out), input, p=p, dim=dim, eps=eps, out=out
        )
    if out is None:
        denom = input.norm(p, dim, keepdim=True).clamp_min(eps).expand_as(input)
        return input / denom
    else:
        denom = input.norm(p, dim, keepdim=True).clamp_min_(eps).expand_as(input)
        return torch.div(input, denom, out=out)


def normalize(i, parentsize):
    if isinstance(i, slice):
        i = (i.start, i.stop, i.step)
    if not isinstance(i, (tuple, list, Tuple)):
        if (i < 0) == True:
            i += parentsize
        i = (i, i+1, 1)
    i = list(i)
    if len(i) == 2:
        i.append(1)
    start, stop, step = i
    start = start or 0
    if stop is None:
        stop = parentsize
    if (start < 0) == True:
        start += parentsize
    if (stop < 0) == True:
        stop += parentsize
    step = step or 1

    if ((stop - start) * step < 1) == True:
        raise IndexError()

    return (start, stop, step)


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower().replace("-", "_")


def normalize(b, a):
    """Normalize numerator/denominator of a continuous-time transfer function.

    If values of `b` are too close to 0, they are removed. In that case, a
    BadCoefficients warning is emitted.

    Parameters
    ----------
    b : array_like
        Numerator of the transfer function. Can be a 2-D array to normalize
        multiple transfer functions.
    a : array_like
        Denominator of the transfer function. At most 1-D.

    Returns
    -------
    num : array
        The numerator of the normalized transfer function. At least a 1-D
        array. A 2-D array if the input `num` is a 2-D array.
    den : 1-D array
        The denominator of the normalized transfer function.

    Notes
    -----
    Coefficients for both the numerator and denominator should be specified in
    descending exponent order (e.g., ``s^2 + 3s + 5`` would be represented as
    ``[1, 3, 5]``).

    Examples
    --------
    >>> from scipy.signal import normalize

    Normalize the coefficients of the transfer function
    ``(3*s^2 - 2*s + 5) / (2*s^2 + 3*s + 1)``:

    >>> b = [3, -2, 5]
    >>> a = [2, 3, 1]
    >>> normalize(b, a)
    (array([ 1.5, -1. ,  2.5]), array([1. , 1.5, 0.5]))

    A warning is generated if, for example, the first coefficient of
    `b` is 0.  In the following example, the result is as expected:

    >>> import warnings
    >>> with warnings.catch_warnings(record=True, action='always') as w:
    ...     num, den = normalize([0, 3, 6], [2, -5, 4])

    >>> num
    array([1.5, 3. ])
    >>> den
    array([ 1. , -2.5,  2. ])

    >>> print(w[0].message)
    Badly conditioned filter coefficients (numerator): the results may be meaningless

    """
    try:
        xp = array_namespace(b, a)
    except TypeError:
        # object arrays, test_ltisys.py::TestSS2TF::test_simo_round_trip
        xp = np_compat

    den = xp.asarray(a)
    den = xpx.atleast_nd(den, ndim=1, xp=xp)

    num = xp.asarray(b)
    num = xpx.atleast_nd(_align_nums(num, xp), ndim=2, xp=xp)

    if den.ndim != 1:
        raise ValueError("Denominator polynomial must be rank-1 array.")
    if num.ndim > 2:
        raise ValueError("Numerator polynomial must be rank-1 or"
                         " rank-2 array.")
    if xp.all(den == 0):
        raise ValueError("Denominator must have at least on nonzero element.")

    # Trim leading zeros in denominator, leave at least one.
    den = _pu._trim_zeros(den, 'f')

    # Normalize transfer function
    num, den = num / den[0], den / den[0]

    # Count numerator columns that are all zero
    leading_zeros = 0
    for j in range(num.shape[-1]):
        col = num[:, j]
        if xp.all(xp.abs(col) <= 1e-14):
            leading_zeros += 1
        else:
            break

    # Trim leading zeros of numerator
    if leading_zeros > 0:
        warnings.warn("Badly conditioned filter coefficients (numerator): the "
                      "results may be meaningless",
                      BadCoefficients, stacklevel=2)
        # Make sure at least one column remains
        if leading_zeros == num.shape[1]:
            leading_zeros -= 1
        num = num[:, leading_zeros:]

    # Squeeze first dimension if singular
    if num.shape[0] == 1:
        num = num[0, :]

    return num, den


def normalize(string, remove=''):
    string = string.lower()
    for char in remove + ' ':
        if char in string:
            string = string.replace(char, '')
    return string


def normalize(idx: Index, shape: Shape) -> Index:
  return tuple(
      slice(
          s.start if s.start is not None else 0,
          s.stop if s.stop is not None else dim,
          s.step if s.step is not None else 1,
      )
      for s, dim in zip(idx, shape)
  )


def normalize() -> base.GradientTransformation:
  """Normalizes the gradient.

  Returns:
    An (init_fn, update_fn) tuple.
  """

  def init_fn(params):
    del params
    return NormalizeState()

  def update_fn(updates, state, params=None):
    del params
    g_norm = optax.tree.norm(updates)
    updates = jax.tree.map(lambda g: g / g_norm, updates)
    return updates, state

  return base.GradientTransformation(init_fn, update_fn)


def normalize(obj):
    """Normalize Expr and apply basic evaluation methods.
    """
    if not isinstance(obj, Expr):
        return obj

    if obj.op is Op.TERMS:
        d = {}
        for t, c in obj.data.items():
            if c == 0:
                continue
            if t.op is Op.COMPLEX and c != 1:
                t = t * c
                c = 1
            if t.op is Op.TERMS:
                for t1, c1 in t.data.items():
                    _pairs_add(d, t1, c1 * c)
            else:
                _pairs_add(d, t, c)
        if len(d) == 0:
            # TODO: determine correct kind
            return as_number(0)
        elif len(d) == 1:
            (t, c), = d.items()
            if c == 1:
                return t
        return Expr(Op.TERMS, d)

    if obj.op is Op.FACTORS:
        coeff = 1
        d = {}
        for b, e in obj.data.items():
            if e == 0:
                continue
            if b.op is Op.TERMS and isinstance(e, integer_types) and e > 1:
                # expand integer powers of sums
                b = b * (b ** (e - 1))
                e = 1

            if b.op in (Op.INTEGER, Op.REAL):
                if e == 1:
                    coeff *= b.data[0]
                elif e > 0:
                    coeff *= b.data[0] ** e
                else:
                    _pairs_add(d, b, e)
            elif b.op is Op.FACTORS:
                if e > 0 and isinstance(e, integer_types):
                    for b1, e1 in b.data.items():
                        _pairs_add(d, b1, e1 * e)
                else:
                    _pairs_add(d, b, e)
            else:
                _pairs_add(d, b, e)
        if len(d) == 0 or coeff == 0:
            # TODO: determine correct kind
            assert isinstance(coeff, number_types)
            return as_number(coeff)
        elif len(d) == 1:
            (b, e), = d.items()
            if e == 1:
                t = b
            else:
                t = Expr(Op.FACTORS, d)
            if coeff == 1:
                return t
            return Expr(Op.TERMS, {t: coeff})
        elif coeff == 1:
            return Expr(Op.FACTORS, d)
        else:
            return Expr(Op.TERMS, {Expr(Op.FACTORS, d): coeff})

    if obj.op is Op.APPLY and obj.data[0] is ArithOp.DIV:
        dividend, divisor = obj.data[1]
        t1, c1 = as_term_coeff(dividend)
        t2, c2 = as_term_coeff(divisor)
        if isinstance(c1, integer_types) and isinstance(c2, integer_types):
            g = gcd(c1, c2)
            c1, c2 = c1 // g, c2 // g
        else:
            c1, c2 = c1 / c2, 1

        if t1.op is Op.APPLY and t1.data[0] is ArithOp.DIV:
            numer = t1.data[1][0] * c1
            denom = t1.data[1][1] * t2 * c2
            return as_apply(ArithOp.DIV, numer, denom)

        if t2.op is Op.APPLY and t2.data[0] is ArithOp.DIV:
            numer = t2.data[1][1] * t1 * c1
            denom = t2.data[1][0] * c2
            return as_apply(ArithOp.DIV, numer, denom)

        d = dict(as_factors(t1).data)
        for b, e in as_factors(t2).data.items():
            _pairs_add(d, b, -e)
        numer, denom = {}, {}
        for b, e in d.items():
            if e > 0:
                numer[b] = e
            else:
                denom[b] = -e
        numer = normalize(Expr(Op.FACTORS, numer)) * c1
        denom = normalize(Expr(Op.FACTORS, denom)) * c2

        if denom.op in (Op.INTEGER, Op.REAL) and denom.data[0] == 1:
            # TODO: denom kind not used
            return numer
        return as_apply(ArithOp.DIV, numer, denom)

    if obj.op is Op.CONCAT:
        lst = [obj.data[0]]
        for s in obj.data[1:]:
            last = lst[-1]
            if (
                    last.op is Op.STRING
                    and s.op is Op.STRING
                    and last.data[0][0] in '"\''
                    and s.data[0][0] == last.data[0][-1]
            ):
                new_last = as_string(last.data[0][:-1] + s.data[0][1:],
                                     max(last.data[1], s.data[1]))
                lst[-1] = new_last
            else:
                lst.append(s)
        if len(lst) == 1:
            return lst[0]
        return Expr(Op.CONCAT, tuple(lst))

    if obj.op is Op.TERNARY:
        cond, expr1, expr2 = map(normalize, obj.data)
        if cond.op is Op.INTEGER:
            return expr1 if cond.data[0] else expr2
        return Expr(Op.TERNARY, (cond, expr1, expr2))

    return obj


def normalize(state: StateCore) -> None:
    # Normalize newlines
    string = NEWLINES_RE.sub("\n", state.src)

    # Replace NULL characters
    string = NULL_RE.sub("\ufffd", string)

    state.src = string


def normalize(text: str) -> str:
    """Lowercase, NFKC, strip zero-width, leetspeak, collapse spaces."""
    if not text or not isinstance(text, str):
        return ""
    t = ZERO_WIDTH.sub("", text)
    t = unicodedata.normalize("NFKC", t).lower().strip()
    for c, r in LEET.items():
        t = t.replace(c, r)
    return re.sub(r"\s+", " ", t)


def normalize(value, triple, avarMapping):
    value = normalizeValue(value, triple)
    if avarMapping:
        value = piecewiseLinearMap(value, avarMapping)
    # Quantize to F2Dot14, to avoid surprise interpolations.
    return floatToFixedToFloat(value, 14)


def normalize(x: FloatArray['*d'], axis: int = -1) -> FloatArray['*d']:
  """Normalize the vector to the unit norm."""
  return x / compat.norm(x, axis=axis, keepdims=True)

