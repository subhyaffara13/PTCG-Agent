import re
from typing import Any, Callable

def _normalize(
    nbdict: Any,
    version: int,
    version_minor: int,
    repair_duplicate_cell_ids: bool,
    relax_add_props: bool,
    strip_invalid_metadata: bool,
) -> tuple[int, Any]:
    """
    Private normalisation routine.

    This function attempts to normalize the `nbdict` passed to it.

    As `_normalize()` is currently used both in `validate()` (for
    historical reasons), and in the `normalize()` public function,
    `_normalize()` does currently mutate `nbdict`.
    Ideally, once `validate()` stops calling `_normalize()`, `_normalize()`
    may stop mutating `nbdict`.

    """
    changes = 0

    if (version, version_minor) >= (4, 5):
        # if we support cell ids ensure default ids are provided
        for cell in nbdict["cells"]:
            if "id" not in cell:
                warnings.warn(
                    "Cell is missing an id field, this will become"
                    " a hard error in future nbformat versions. You may want"
                    " to use `normalize()` on your notebooks before validations"
                    " (available since nbformat 5.1.4). Previous versions of nbformat"
                    " are fixing this issue transparently, and will stop doing so"
                    " in the future.",
                    MissingIDFieldWarning,
                    stacklevel=3,
                )
                # Generate cell ids if any are missing
                if repair_duplicate_cell_ids:
                    cell["id"] = generate_corpus_id()
                    changes += 1

        # if we support cell ids check for uniqueness when validating the whole notebook
        seen_ids = set()
        for cell in nbdict["cells"]:
            if "id" not in cell:
                continue
            cell_id = cell["id"]
            if cell_id in seen_ids:
                # Best effort to repair if we find a duplicate id
                if repair_duplicate_cell_ids:
                    new_id = generate_corpus_id()
                    cell["id"] = new_id
                    changes += 1
                    warnings.warn(
                        f"Non-unique cell id {cell_id!r} detected. Corrected to {new_id!r}.",
                        DuplicateCellId,
                        stacklevel=3,
                    )
                else:
                    msg = f"Non-unique cell id '{cell_id}' detected."
                    raise ValidationError(msg)
            seen_ids.add(cell_id)
    if strip_invalid_metadata:
        changes += _strip_invalida_metadata(
            nbdict, version, version_minor, relax_add_props=relax_add_props
        )
    return changes, nbdict


def _normalize(
    lhs: str, rhs: str | AbstractSet[str], key: str
) -> tuple[str, str | AbstractSet[str]]:
    # PEP 685 - Comparison of extra names for optional distribution dependencies
    # https://peps.python.org/pep-0685/
    # > When comparing extra names, tools MUST normalize the names being
    # > compared using the semantics outlined in PEP 503 for names
    if key == "extra":
        assert isinstance(rhs, str), "extra value must be a string"
        # Both sides are normalized at this point already
        return (lhs, rhs)
    if key in MARKERS_ALLOWING_SET:
        if isinstance(rhs, str):  # pragma: no cover
            return (canonicalize_name(lhs), canonicalize_name(rhs))
        else:
            return (canonicalize_name(lhs), {canonicalize_name(v) for v in rhs})

    # other environment markers don't have such standards
    return lhs, rhs


def _normalize(
    a: Tensor, norm_dims: DimsType, eps: float
) -> tuple[Tensor, Tensor, Tensor]:
    """Computes mean and 1/std of a tensor along norm_dims.

    Used as a helper function for normalization layers.

    Args:
        a (Tensor): input tensor
        norm_dims (DimsType): dimensions to normalize over
        eps (float): epsilon for numerical stability

    Returns:
        out (Tensor): normalized tensor.
        mean (Tensor): mean of the tensor along norm_dims.
        rstd (Tensor): 1/std of the tensor along norm_dims.
    """

    norm_dims = utils.canonicalize_dims(a.ndim, norm_dims)
    computation_dtype = utils.get_computation_dtype(a.dtype)
    a_acc = _maybe_convert_to_dtype(a, computation_dtype)
    if not isinstance(a_acc, TensorLike):
        raise AssertionError(f"a_acc must be TensorLike, got {type(a_acc)}")
    biased_var, mean = torch.var_mean(
        a_acc, dim=norm_dims, unbiased=False, keepdim=True
    )
    rstd = torch.rsqrt(biased_var + eps)
    out = (a_acc - mean) * rstd
    return out, mean, rstd


def _normalize(list_of, parent, negative=True):
    """
    Normalize a given annihilator
    """

    num = []
    denom = []
    base = parent.base
    K = base.get_field()
    lcm_denom = base.from_sympy(S.One)
    list_of_coeff = []

    # convert polynomials to the elements of associated
    # fraction field
    for i, j in enumerate(list_of):
        if isinstance(j, base.dtype):
            list_of_coeff.append(K.new(j.to_list()))
        elif not isinstance(j, K.dtype):
            list_of_coeff.append(K.from_sympy(sympify(j)))
        else:
            list_of_coeff.append(j)

        # corresponding numerators of the sequence of polynomials
        num.append(list_of_coeff[i].numer())

        # corresponding denominators
        denom.append(list_of_coeff[i].denom())

    # lcm of denominators in the coefficients
    for i in denom:
        lcm_denom = i.lcm(lcm_denom)

    if negative:
        lcm_denom = -lcm_denom

    lcm_denom = K.new(lcm_denom.to_list())

    # multiply the coefficients with lcm
    for i, j in enumerate(list_of_coeff):
        list_of_coeff[i] = j * lcm_denom

    gcd_numer = base((list_of_coeff[-1].numer() / list_of_coeff[-1].denom()).to_list())

    # gcd of numerators in the coefficients
    for i in num:
        gcd_numer = i.gcd(gcd_numer)

    gcd_numer = K.new(gcd_numer.to_list())

    # divide all the coefficients by the gcd
    for i, j in enumerate(list_of_coeff):
        frac_ans = j / gcd_numer
        list_of_coeff[i] = base((frac_ans.numer() / frac_ans.denom()).to_list())

    return DifferentialOperator(list_of_coeff, parent)


def _normalize(
    lhs: str, rhs: str | AbstractSet[str], key: str
) -> tuple[str, str | AbstractSet[str]]:
    # PEP 685 - Comparison of extra names for optional distribution dependencies
    # https://peps.python.org/pep-0685/
    # > When comparing extra names, tools MUST normalize the names being
    # > compared using the semantics outlined in PEP 503 for names
    if key == "extra":
        assert isinstance(rhs, str), "extra value must be a string"
        # Both sides are normalized at this point already
        return (lhs, rhs)
    if key in MARKERS_ALLOWING_SET:
        if isinstance(rhs, str):  # pragma: no cover
            return (canonicalize_name(lhs), canonicalize_name(rhs))
        else:
            return (canonicalize_name(lhs), {canonicalize_name(v) for v in rhs})

    # other environment markers don't have such standards
    return lhs, rhs


def _normalize(
    lhs: str, rhs: str | AbstractSet[str], key: str
) -> tuple[str, str | AbstractSet[str]]:
    # PEP 685 - Comparison of extra names for optional distribution dependencies
    # https://peps.python.org/pep-0685/
    # > When comparing extra names, tools MUST normalize the names being
    # > compared using the semantics outlined in PEP 503 for names
    if key == "extra":
        assert isinstance(rhs, str), "extra value must be a string"
        # Both sides are normalized at this point already
        return (lhs, rhs)
    if key in MARKERS_ALLOWING_SET:
        if isinstance(rhs, str):  # pragma: no cover
            return (canonicalize_name(lhs), canonicalize_name(rhs))
        else:
            return (canonicalize_name(lhs), {canonicalize_name(v) for v in rhs})

    # other environment markers don't have such standards
    return lhs, rhs


def _normalize(
    table: DataFrame, normalize, margins: bool, margins_name: Hashable = "All"
) -> DataFrame:
    if not isinstance(normalize, (bool, str)):
        axis_subs = {0: "index", 1: "columns"}
        try:
            normalize = axis_subs[normalize]
        except KeyError as err:
            raise ValueError("Not a valid normalize argument") from err

    if margins is False:
        # Actual Normalizations
        normalizers: dict[bool | str, Callable] = {
            "all": lambda x: x / x.sum(axis=1).sum(axis=0),
            "columns": lambda x: x / x.sum(),
            "index": lambda x: x.div(x.sum(axis=1), axis=0),
        }

        normalizers[True] = normalizers["all"]

        try:
            f = normalizers[normalize]
        except KeyError as err:
            raise ValueError("Not a valid normalize argument") from err

        table = f(table)
        table = table.fillna(0)

    elif margins is True:
        # keep index and column of pivoted table
        table_index = table.index
        table_columns = table.columns
        last_ind_or_col = table.iloc[-1, :].name

        # check if margin name is not in (for MI cases) and not equal to last
        # index/column and save the column and index margin
        if (margins_name not in last_ind_or_col) & (margins_name != last_ind_or_col):
            raise ValueError(f"{margins_name} not in pivoted DataFrame")
        column_margin = table.iloc[:-1, -1]
        index_margin = table.iloc[-1, :-1]

        # keep the core table
        table = table.iloc[:-1, :-1]

        # Normalize core
        table = _normalize(table, normalize=normalize, margins=False)

        # Fix Margins
        if normalize == "columns":
            column_margin = column_margin / column_margin.sum()
            table = concat([table, column_margin], axis=1)
            table = table.fillna(0)
            table.columns = table_columns

        elif normalize == "index":
            index_margin = index_margin / index_margin.sum()
            table = table._append_internal(index_margin, ignore_index=True)
            table = table.fillna(0)
            table.index = table_index

        elif normalize == "all" or normalize is True:
            column_margin = column_margin / column_margin.sum()
            index_margin = index_margin / index_margin.sum()
            index_margin.loc[margins_name] = 1
            table = concat([table, column_margin], axis=1)
            table = table._append_internal(index_margin, ignore_index=True)

            table = table.fillna(0)
            table.index = table_index
            table.columns = table_columns

        else:
            raise ValueError("Not a valid normalize argument")

    else:
        raise ValueError("Not a valid margins argument")

    return table


def _normalize(sign, man, exp, bc, prec, rnd):
    """
    Create a raw mpf tuple with value (-1)**sign * man * 2**exp and
    normalized mantissa. The mantissa is rounded in the specified
    direction if its size exceeds the precision. Trailing zero bits
    are also stripped from the mantissa to ensure that the
    representation is canonical.

    Conditions on the input:
    * The input must represent a regular (finite) number
    * The sign bit must be 0 or 1
    * The mantissa must be positive
    * The exponent must be an integer
    * The bitcount must be exact

    If these conditions are not met, use from_man_exp, mpf_pos, or any
    of the conversion functions to create normalized raw mpf tuples.
    """
    if not man:
        return fzero
    # Cut mantissa down to size if larger than target precision
    n = bc - prec
    if n > 0:
        if rnd == round_nearest:
            t = man >> (n-1)
            if t & 1 and ((t & 2) or (man & h_mask[n<300][n])):
                man = (t>>1)+1
            else:
                man = t>>1
        elif shifts_down[rnd][sign]:
            man >>= n
        else:
            man = -((-man)>>n)
        exp += n
        bc = prec
    # Strip trailing bits
    if not man & 1:
        t = trailtable[int(man & 255)]
        if not t:
            while not man & 255:
                man >>= 8
                exp += 8
                bc -= 8
            t = trailtable[int(man & 255)]
        man >>= t
        exp += t
        bc -= t
    # Bit count can be wrong if the input mantissa was 1 less than
    # a power of 2 and got rounded up, thereby adding an extra bit.
    # With trailing bits removed, all powers of two have mantissa 1,
    # so this is easy to check for.
    if man == 1:
        bc = 1
    return sign, man, exp, bc


def _normalize(move: str) -> str:
    """Lowercase, strip whitespace and parentheses (so 'A1' or '(a, 1)' work)."""
    cleaned = re.sub(r"[\s()\[\],.]", "", move).lower()
    return cleaned


def _normalize(move: str) -> str:
    """Lowercase and drop whitespace/punctuation for forgiving comparisons."""
    return re.sub(r"[\s,.\-_'\"`()\[\]]", "", move).lower()


def _normalize(move: str) -> str:
    """Strip whitespace and lowercase a candidate move string."""
    return re.sub(r"\s+", "", move).lower()


def _normalize(move: str) -> str:
    return re.sub(r"\s+", "", move).lower()


def _normalize(
  mdl: Module,
  x: Array,
  mean: Array,
  var: Array,
  reduction_axes: Axes,
  feature_axes: Axes,
  dtype: Dtype | None,
  param_dtype: Dtype,
  epsilon: float,
  use_bias: bool,
  use_scale: bool,
  bias_init: Initializer,
  scale_init: Initializer,
  force_float32_reductions: bool = True
):
  """Normalizes the input of a normalization layer and optionally applies a learned scale and bias.

  Arguments:
    mdl: Module to apply the normalization in (normalization params will reside
      in this module).
    x: The input.
    mean: Mean to use for normalization.
    var: Variance to use for normalization.
    reduction_axes: The axes in ``x`` to reduce.
    feature_axes: Axes containing features. A separate bias and scale is learned
      for each specified feature.
    dtype: The dtype of the result (default: infer from input and params).
    param_dtype: The dtype of the parameters.
    epsilon: Normalization epsilon.
    use_bias: If true, add a bias term to the output.
    use_scale: If true, scale the output.
    bias_init: Initialization function for the bias term.
    scale_init: Initialization function for the scaling function.
    force_float32_reductions: If false, the scale and bias parameters use the
      param_dtype. Otherwise, they will have at least float32 precision due to
      the mean and var being promoted to float32.

  Returns:
    The normalized input.
  """
  reduction_axes = _canonicalize_axes(x.ndim, reduction_axes)
  feature_axes = _canonicalize_axes(x.ndim, feature_axes)
  feature_shape = [1] * x.ndim
  reduced_feature_shape = []
  for ax in feature_axes:
    feature_shape[ax] = x.shape[ax]
    reduced_feature_shape.append(x.shape[ax])

  mean = jnp.expand_dims(mean, reduction_axes)
  var = jnp.expand_dims(var, reduction_axes)
  y = x - mean
  mul = lax.rsqrt(var + epsilon)
  args = [x]
  if use_scale:
    scale = mdl.param(
      'scale', scale_init, reduced_feature_shape, param_dtype
    ).reshape(feature_shape)
    if not force_float32_reductions:
      scale = jnp.asarray(scale, param_dtype)
    mul *= scale
    args.append(scale)
  y *= mul
  if use_bias:
    bias = mdl.param(
      'bias', bias_init, reduced_feature_shape, param_dtype
    ).reshape(feature_shape)
    if not force_float32_reductions:
      bias = jnp.asarray(bias, param_dtype)
    y += bias
    args.append(bias)
  dtype = dtypes.canonicalize_dtype(*args, dtype=dtype)
  return jnp.asarray(y, dtype)


def _normalize(
  x: Array,
  mean: Array,
  var: Array,
  scale: tp.Optional[Array],
  bias: tp.Optional[Array],
  reduction_axes: Axes,
  feature_axes: Axes,
  dtype: tp.Optional[Dtype],
  epsilon: float,
):
  """ "Normalizes the input of a normalization layer and optionally applies a learned scale and bias.

  Arguments:
    x: The input.
    mean: Mean to use for normalization.
    var: Variance to use for normalization.
    reduction_axes: The axes in ``x`` to reduce.
    feature_axes: Axes containing features. A separate bias and scale is learned
      for each specified feature.
    dtype: The dtype of the result (default: infer from input and params).
    epsilon: Normalization epsilon.

  Returns:
    The normalized input.
  """
  reduction_axes = _canonicalize_axes(x.ndim, reduction_axes)
  feature_axes = _canonicalize_axes(x.ndim, feature_axes)
  stats_shape = list(x.shape)
  for axis in reduction_axes:
    stats_shape[axis] = 1
  mean = mean.reshape(stats_shape)
  var = var.reshape(stats_shape)
  feature_shape = [1] * x.ndim
  for ax in feature_axes:
    feature_shape[ax] = x.shape[ax]
  y = x - mean
  mul = lax.rsqrt(var + epsilon)
  args = [x]
  if scale is not None:
    scale = scale.reshape(feature_shape)
    mul *= scale
    args.append(scale)
  y *= mul
  if bias is not None:
    bias = bias.reshape(feature_shape)
    y += bias
    args.append(bias)
  dtype = dtypes.canonicalize_dtype(*args, dtype=dtype)
  return jnp.asarray(y, dtype)


def _normalize(
  mdl: nn.Module,
  x: Array,
  mean: Array,
  var: Array,
  reduction_axes: Axes,
  feature_axes: Axes,
  dtype: Dtype,
  param_dtype: Dtype,
  epsilon: float,
  use_bias: bool,
  use_scale: bool,
  bias_init: Initializer,
  scale_init: Initializer,
):
  """ "Normalizes the input of a normalization layer and optionally applies a learned scale and bias.

  A separate bias and scale is learned for each feature as specified by
  feature_axes.
  """
  reduction_axes = _canonicalize_axes(x.ndim, reduction_axes)
  feature_axes = _canonicalize_axes(x.ndim, feature_axes)
  stats_shape = list(x.shape)
  for axis in reduction_axes:
    stats_shape[axis] = 1
  mean = mean.reshape(stats_shape)
  var = var.reshape(stats_shape)
  feature_shape = [1] * x.ndim
  reduced_feature_shape = []
  for ax in feature_axes:
    feature_shape[ax] = x.shape[ax]
    reduced_feature_shape.append(x.shape[ax])
  y = x - mean
  mul = lax.rsqrt(var + epsilon)
  if use_scale:
    scale = mdl.param_with_axes(
      'scale', scale_init, reduced_feature_shape, param_dtype, axes=('embed',)
    ).reshape(feature_shape)
    mul *= scale
  y *= mul
  if use_bias:
    bias = mdl.param_with_axes(
      'bias', bias_init, reduced_feature_shape, param_dtype, axes=('embed',)
    ).reshape(feature_shape)
    y += bias
  return jnp.asarray(y, dtype)

