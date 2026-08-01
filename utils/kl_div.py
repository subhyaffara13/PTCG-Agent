
def kl_div(
    input: Tensor,
    target: Tensor,
    size_average: bool | None = None,
    reduce: bool | None = None,
    reduction: str = "mean",
    log_target: bool = False,
) -> Tensor:
    r"""Compute the KL Divergence loss.

    Refer - The `Kullback-Leibler divergence Loss
    <https://en.wikipedia.org/wiki/Kullback-Leibler_divergence>`__

    See :class:`~torch.nn.KLDivLoss` for details.

    Args:
        input: Tensor of arbitrary shape in log-probabilities.
        target: Tensor of the same shape as input. See :attr:`log_target` for
            the target's interpretation.
        size_average (bool, optional): Deprecated (see :attr:`reduction`).
        reduce (bool, optional): Deprecated (see :attr:`reduction`).
        reduction (str, optional): Specifies the reduction to apply to the output:
            ``'none'`` | ``'batchmean'`` | ``'sum'`` | ``'mean'``.
            ``'none'``: no reduction will be applied
            ``'batchmean'``: the sum of the output will be divided by the batchsize
            ``'sum'``: the output will be summed
            ``'mean'``: the output will be divided by the number of elements in the output
            Default: ``'mean'``
        log_target (bool): A flag indicating whether ``target`` is passed in the log space.
            It is recommended to pass certain distributions (like ``softmax``)
            in the log space to avoid numerical issues caused by explicit ``log``.
            Default: ``False``

    .. note::
        :attr:`size_average` and :attr:`reduce` are in the process of being deprecated,
        and in the meantime, specifying either of those two args will override :attr:`reduction`.

    .. warning::
        :attr:`reduction` = ``'mean'`` doesn't return the true kl divergence value, please use
        :attr:`reduction` = ``'batchmean'`` which aligns with KL math definition.
    """
    if has_torch_function_variadic(input, target):
        return handle_torch_function(
            kl_div,
            (input, target),
            input,
            target,
            size_average=size_average,
            reduce=reduce,
            reduction=reduction,
            log_target=log_target,
        )
    if size_average is not None or reduce is not None:
        reduction_enum = _Reduction.legacy_get_enum(size_average, reduce)
    else:
        if reduction == "mean":
            warnings.warn(
                "reduction: 'mean' divides the total loss by both the batch size and the support size."
                "'batchmean' divides only by the batch size, and aligns with the KL div math definition."
                "'mean' will be changed to behave the same as 'batchmean' in the next major release.",
                stacklevel=2,
            )

        # special case for batchmean
        if reduction == "batchmean":
            reduction_enum = _Reduction.get_enum("sum")
        else:
            reduction_enum = _Reduction.get_enum(reduction)

    reduced = torch.kl_div(input, target, reduction_enum, log_target=log_target)

    if reduction == "batchmean" and input.dim() != 0:
        reduced = reduced / input.size()[0]

    return reduced


def kl_div(g: jit_utils.GraphContext, input, target, reduction, log_target):
    if log_target:
        output = _kl_div_log_target_impl(g, input, target)
    else:
        output = _kl_div_non_log_target_impl(g, input, target)

    if reduction == 0:
        return output
    elif reduction == 1:
        return g.op("ReduceMean", output, keepdims_i=0)
    elif reduction == 2:
        return symbolic_helper._reducesum_helper(g, output, keepdims_i=0)
    else:
        return symbolic_helper._onnx_unsupported(
            "kl_div with reduction other than none, mean, or sum.", input
        )


def kl_div(
    p: ArrayLike,
    q: ArrayLike,
) -> Array:
  r"""The Kullback-Leibler divergence.

  JAX implementation of :obj:`scipy.special.kl_div`.

  .. math::

     \mathrm{kl\_div}(p, q) = \begin{cases}
       p\log(p/q)-p+q & p>0,q>0\\
       q & p=0,q\ge 0\\
       \infty & \mathrm{otherwise}
    \end{cases}

  Args:
    p: arraylike, real-valued.
    q: arraylike, real-valued.

  Returns:
    array of KL-divergence values

  See also:
    - :func:`jax.scipy.special.entr`
    - :func:`jax.scipy.special.rel_entr`
  """
  p, q = promote_args_inexact("kl_div", p, q)
  if dtypes.issubdtype(p.dtype, np.complexfloating):
    raise ValueError("kl_div does not support complex-valued inputs.")
  return rel_entr(p, q) - p + q

