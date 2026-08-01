
def ctc_loss(
    log_probs: Tensor,
    targets: Tensor,
    input_lengths: Tensor,
    target_lengths: Tensor,
    blank: int = 0,
    reduction: str = "mean",
    zero_infinity: bool = False,
) -> Tensor:
    r"""Compute the Connectionist Temporal Classification loss.

    See :class:`~torch.nn.CTCLoss` for details.

    Note:
        {cudnn_reproducibility_note}

    Note:
        {backward_reproducibility_note}

    Args:
        log_probs: :math:`(T, N, C)` or :math:`(T, C)` where `C = number of characters in alphabet including blank`,
            `T = input length`, and `N = batch size`.
            The logarithmized probabilities of the outputs
            (e.g. obtained with :func:`torch.nn.functional.log_softmax`).
        targets: :math:`(N, S)` or `(sum(target_lengths))`.
                May be an empty tensor if all entries in `target_lengths` are zero.
                In the second form, the targets are assumed to be concatenated.
        input_lengths: :math:`(N)` or :math:`()`.
            Lengths of the inputs (must each be :math:`\leq T`)
        target_lengths: :math:`(N)` or :math:`()`.
            Lengths of the targets
        blank (int, optional):
            Blank label. Default :math:`0`.
        reduction (str, optional): Specifies the reduction to apply to the output:
            ``'none'`` | ``'mean'`` | ``'sum'``. ``'none'``: no reduction will be applied,
            ``'mean'``: the output losses will be divided by the target lengths and
            then the mean over the batch is taken, ``'sum'``: the output will be
            summed. Default: ``'mean'``
        zero_infinity (bool, optional):
            Whether to zero infinite losses and the associated gradients.
            Default: ``False``
            Infinite losses mainly occur when the inputs are too short
            to be aligned to the targets.

    Example::

        >>> log_probs = torch.randn(50, 16, 20).log_softmax(2).detach().requires_grad_()
        >>> targets = torch.randint(1, 20, (16, 30), dtype=torch.long)
        >>> input_lengths = torch.full((16,), 50, dtype=torch.long)
        >>> target_lengths = torch.randint(10, 30, (16,), dtype=torch.long)
        >>> loss = F.ctc_loss(log_probs, targets, input_lengths, target_lengths)
        >>> loss.backward()
    """
    if has_torch_function_variadic(log_probs, targets, input_lengths, target_lengths):
        return handle_torch_function(
            ctc_loss,
            (log_probs, targets, input_lengths, target_lengths),
            log_probs,
            targets,
            input_lengths,
            target_lengths,
            blank=blank,
            reduction=reduction,
            zero_infinity=zero_infinity,
        )
    return torch.ctc_loss(
        log_probs,
        targets,
        input_lengths,
        target_lengths,
        blank,
        _Reduction.get_enum(reduction),
        zero_infinity,
    )


def ctc_loss(
    logits: jax.typing.ArrayLike,
    logit_paddings: jax.typing.ArrayLike,
    labels: jax.typing.ArrayLike,
    label_paddings: jax.typing.ArrayLike,
    *,
    blank_id: int = 0,
    log_epsilon: jax.typing.ArrayLike = -1e5,
) -> jax.Array:
  """Computes CTC loss.

  See docstring for ``ctc_loss_with_forward_probs`` for details.

  Args:
    logits: (B, T, K)-array containing logits of each class where B denotes the
      batch size, T denotes the max time frames in ``logits``, and K denotes the
      number of classes including a class for blanks.
    logit_paddings: (B, T)-array. Padding indicators for ``logits``. Each
      element must be either 1.0 or 0.0, and ``logitpaddings[b, t] == 1.0``
      denotes that ``logits[b, t, :]`` are padded values.
    labels: (B, N)-array containing reference integer labels where N denotes the
      max time frames in the label sequence.
    label_paddings: (B, N)-array. Padding indicators for ``labels``. Each
      element must be either 1.0 or 0.0, and ``labelpaddings[b, n] == 1.0``
      denotes that ``labels[b, n]`` is a padded label. In the current
      implementation, ``labels`` must be right-padded, i.e. each row
      ``labelpaddings[b, :]`` must be repetition of zeroes, followed by
      repetition of ones.
    blank_id: Id for blank token. ``logits[b, :, blank_id]`` are used as
      probabilities of blank symbols.
    log_epsilon: Numerically-stable approximation of log(+0).

  Returns:
    (B,)-array containing loss values for each sequence in the batch.
  """
  per_seq_loss, _, _ = ctc_loss_with_forward_probs(
      logits,
      logit_paddings,
      labels,
      label_paddings,
      blank_id=blank_id,
      log_epsilon=log_epsilon,
  )
  return per_seq_loss

