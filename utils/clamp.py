
def clamp(
    value: float,
    format: str = "{:}",
    floor: float | None = None,
    ceil: float | None = None,
    floor_token: str = "<",
    ceil_token: str = ">",
) -> str:
    """Returns number with the specified format, clamped between floor and ceil.

    If the number is larger than ceil or smaller than floor, then the respective limit
    will be returned, formatted and prepended with a token specifying as such.

    Examples:
        ```pycon
        >>> clamp(123.456)
        '123.456'
        >>> clamp(0.0001, floor=0.01)
        '<0.01'
        >>> clamp(0.99, format="{:.0%}", ceil=0.99)
        '99%'
        >>> clamp(0.999, format="{:.0%}", ceil=0.99)
        '>99%'
        >>> clamp(1, format=intword, floor=1e6, floor_token="under ")
        'under 1.0 million'
        >>> clamp(None) is None
        True

        ```

    Args:
        value (int, float): Input number.
        format (str OR callable): Can either be a formatting string, or a callable
            function that receives value and returns a string.
        floor (int, float): Smallest value before clamping.
        ceil (int, float): Largest value before clamping.
        floor_token (str): If value is smaller than floor, token will be prepended
            to output.
        ceil_token (str): If value is larger than ceil, token will be prepended
            to output.

    Returns:
        str: Formatted number. The output is clamped between the indicated floor and
            ceil. If the number is larger than ceil or smaller than floor, the output
            will be prepended with a token indicating as such.

    """
    import math

    if value is None:
        return None

    if not math.isfinite(value):
        return _format_not_finite(value)

    if floor is not None and value < floor:
        value = floor
        token = floor_token
    elif ceil is not None and value > ceil:
        value = ceil
        token = ceil_token
    else:
        token = ""

    if isinstance(format, str):
        return token + format.format(value)

    if callable(format):
        return token + format(value)

    msg = (
        "Invalid format. Must be either a valid formatting string, or a function "
        "that accepts value and returns a string."
    )
    raise ValueError(msg)


def clamp(
    x: torch.Tensor,
    min: torch.types.Number | None = None,
    max: torch.types.Number | None = None,
) -> torch.Tensor:
    if min is not None:
        x = x.clamp_min(min)
    if max is not None:
        x = x.clamp_max(max)
    return x


def clamp(a, min, max):
    return ops.maximum(min, ops.minimum(max, a))


def clamp(
    a: TensorLikeType,
    min: TensorOrNumberLikeType | None = None,
    max: TensorOrNumberLikeType | None = None,
) -> TensorLikeType:
    # NOTE: grad behavior with implementation `where` is not consistent on `nan`
    if min is None and max is None:
        msg = "clamp called but both min and max are none!"
        raise ValueError(msg)

    if min is not None:
        a_isnan = torch.isnan(a)
        condition = torch.bitwise_or(torch.ge(a, min), a_isnan)  # type: ignore[arg-type]
        # we should also propagate `nan` coming from boundaries. However, that's
        # not necessary since `ge` would already `False` when either operands has
        # a `nan`. So this line below is redundant
        #   `condition = bitwise_and(condition, bitwise_not(isnan(min)))`
        a = torch.where(condition, a, min)  # type: ignore[arg-type]
    if max is not None:
        a_isnan = torch.isnan(a)
        # same as above, no need to adjust `nan` from `max`
        condition = torch.bitwise_or(torch.le(a, max), a_isnan)  # type: ignore[arg-type]
        a = torch.where(condition, a, max)  # type: ignore[arg-type]

    return a


def clamp(g: jit_utils.GraphContext, self, min, max):
    def _cast_if_not_none(tensor, dtype):
        if tensor is not None and not symbolic_helper._is_none(tensor):
            return g.op(
                "Cast",
                tensor,
                to_i=dtype.onnx_type(),
            )
        else:
            return tensor

    scalar_type = _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.UNDEFINED
    )
    if scalar_type != _type_utils.JitScalarType.UNDEFINED:
        min = _cast_if_not_none(min, scalar_type)
        max = _cast_if_not_none(max, scalar_type)

    if symbolic_helper._is_none(min):
        return clamp_max(g, self, max)
    elif symbolic_helper._is_none(max):
        return clamp_min(g, self, min)
    else:
        if (
            symbolic_helper._get_tensor_rank(min) == 0
            and symbolic_helper._get_tensor_rank(max) == 0
        ):
            return symbolic_helper._op_with_optional_float_cast(
                g, "Clip", self, min, max, opset_before=12
            )
        else:
            return clamp_max(g, clamp_min(g, self, min), max)


def clamp(g: jit_utils.GraphContext, self, min, max):
    # min or max may be None that we need to dispatch to
    # Clip separately, as ONNX does not have None syntax
    if symbolic_helper._is_none(min):
        return clamp_max(g, self, max)
    elif symbolic_helper._is_none(max):
        return clamp_min(g, self, min)
    else:
        if symbolic_helper._is_constant(min) and symbolic_helper._is_constant(max):
            return symbolic_helper._op_with_optional_float_cast(
                g,
                "Clip",
                self,
                min_f=symbolic_helper._parse_arg(min, "f"),
                max_f=symbolic_helper._parse_arg(max, "f"),
                opset_before=12,
            )
        else:
            return clamp_max(g, clamp_min(g, self, min), max)


def clamp(input: Tensor, min_: float, max_: float) -> Tensor:
    r"""float(input, min\_, max\_) -> Tensor

    Applies the clamp function element-wise.
    See :class:`~torch.ao.nn.quantized.clamp` for more details.

    Args:
        input: quantized input
        min_: minimum value for clamping
        max_: maximum value for clamping
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.clamp' must be quantized!")
    return torch.clamp(input, min_, max_)


def clamp(min: _ods_ir.Value[_ods_ir.RankedTensorType], operand: _ods_ir.Value[_ods_ir.RankedTensorType], max: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ClampOp(min=min, operand=operand, max=max, results=results, loc=loc, ip=ip).result


def clamp(min: _ods_ir.Value[_ods_ir.RankedTensorType], operand: _ods_ir.Value[_ods_ir.RankedTensorType], max: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ClampOp(min=min, operand=operand, max=max, results=results, loc=loc, ip=ip).result


def clamp(min, operand, max):
  return np.clip(operand, np.clip(min, None, max), max).astype(operand.dtype)


def clamp(min: ArrayLike, x: ArrayLike, max: ArrayLike) -> Array:
  r"""Elementwise clamp.

  Returns :math:`\mathrm{clamp}(x) = \begin{cases}
  \mathit{min} & \text{if } x < \mathit{min},\\
  \mathit{max} & \text{if } x > \mathit{max},\\
  x & \text{otherwise}
  \end{cases}`.
  """
  min, x, max = core.auto_insert_reshard(min, x, max)
  return clamp_p.bind(min, x, max)


def clamp(value, minimum, maximum):
    return min(max(value, minimum), maximum)

