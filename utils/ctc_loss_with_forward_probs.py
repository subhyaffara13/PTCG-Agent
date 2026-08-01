
def ctc_loss_with_forward_probs(
    logits: jax.typing.ArrayLike,
    logit_paddings: jax.typing.ArrayLike,
    labels: jax.typing.ArrayLike,
    label_paddings: jax.typing.ArrayLike,
    *,
    blank_id: int = 0,
    log_epsilon: jax.typing.ArrayLike = -1e5,
) -> tuple[jax.Array, jax.Array, jax.Array]:
  r"""Computes CTC loss and CTC forward-probabilities.

  The CTC loss is a loss function based on log-likelihoods of the model that
  introduces a special blank symbol :math:`\phi` to represent variable-length
  output sequences.

  Forward probabilities returned by this function, as auxiliary results, are
  grouped into two part: blank alpha-probability and non-blank alpha
  probability. Those are defined as follows:

  .. math::
    \alpha_{\mathrm{BLANK}}(t, n) =
    \sum_{\pi_{1:t-1}} p(\pi_t = \phi | \pi_{1:t-1}, y_{1:n-1}, \cdots), \\
    \alpha_{\mathrm{LABEL}}(t, n) =
    \sum_{\pi_{1:t-1}} p(\pi_t = y_n | \pi_{1:t-1}, y_{1:n-1}, \cdots).

  Here, :math:`\pi` denotes the alignment sequence in the reference
  [Graves et al, 2006] that is blank-inserted representations of ``labels``.
  The return values are the logarithms of the above probabilities.

  Args:
    logits: (B, T, K)-array containing logits of each class where B denotes
      the batch size, T denotes the max time frames in ``logits``, and K
      denotes the number of classes including a class for blanks.
    logit_paddings: (B, T)-array. Padding indicators for ``logits``. Each
      element must be either 1.0 or 0.0, and ``logitpaddings[b, t] == 1.0``
      denotes that ``logits[b, t, :]`` are padded values.
    labels: (B, N)-array containing reference integer labels where N denotes
      the max time frames in the label sequence.
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
    A tuple ``(loss_value, logalpha_blank, logalpha_nonblank)``. Here,
    ``loss_value`` is a (B,)-array containing the loss values for each sequence
    in the batch, ``logalpha_blank`` and ``logalpha_nonblank`` are
    (T, B, N+1)-arrays where the (t, b, n)-th element denotes
    \log \alpha_B(t, n) and \log \alpha_L(t, n), respectively, for ``b``-th
    sequence in the batch.

  References:
    Graves et al, `Connectionist temporal classification: labelling unsegmented
    sequence data with recurrent neural networks
    <https://dl.acm.org/doi/abs/10.1145/1143844.1143891>`_, 2006
  """

  utils.check_rank(logits, 3)
  utils.check_rank(labels, 2)
  utils.check_shapes_equal(labels, label_paddings)
  utils.check_shapes_equal(logits[..., 0], logit_paddings)
  batchsize, unused_maxinputlen, num_classes = logits.shape  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  batchsize_of_labels, maxlabellen = labels.shape  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  if batchsize_of_labels != batchsize:
    raise ValueError(
        f'Expected `labels` to have batch size {batchsize}, got'
        f' {batchsize_of_labels}.'
    )

  logprobs = jax.nn.log_softmax(logits)
  labellens = maxlabellen - jnp.sum(label_paddings, axis=1).astype(jnp.int32)

  # repeat[b, n] == 1.0 when label[b, n] == label[b, n+1].
  repeat = (labels[:, :-1] == labels[:, 1:]).astype(jnp.float32)
  repeat = jnp.pad(repeat, ((0, 0), (0, 1)))

  logprobs_phi = logprobs[:, :, blank_id : blank_id + 1]  # [B, T, 1]
  logprobs_phi = jnp.transpose(logprobs_phi, (1, 0, 2))  # [T, B, 1]

  one_hot = jax.nn.one_hot(labels, num_classes=num_classes)  # [B, N, K]
  logprobs_emit = jnp.einsum('btk,bnk->btn', logprobs, one_hot)
  logprobs_emit = jnp.transpose(logprobs_emit, (1, 0, 2))  # [T, B, N]

  logalpha_phi_init = (
      jnp.ones((batchsize, maxlabellen + 1)) * log_epsilon
  )  # [B, N]
  logalpha_phi_init = logalpha_phi_init.at[:, 0].set(0.0)
  logalpha_emit_init = jnp.ones((batchsize, maxlabellen)) * log_epsilon

  def update_phi_score(phi, added_score):
    # Update `phi[:, 1:]`` with adding `added_score` in log space.
    return jnp.concatenate(
        [phi[:, :1], jnp.logaddexp(phi[:, 1:], added_score)], axis=-1
    )

  def loop_body(prev, x):
    prev_phi, prev_emit = prev
    # emit-to-phi epsilon transition, except if the next label is repetition
    prev_phi_orig = prev_phi
    prev_phi = update_phi_score(prev_phi, prev_emit + log_epsilon * repeat)

    logprob_emit, logprob_phi, pad = x

    # phi-to-emit transition
    next_emit = jnp.logaddexp(
        prev_phi[:, :-1] + logprob_emit, prev_emit + logprob_emit
    )
    # self-loop transition
    next_phi = prev_phi + logprob_phi
    # emit-to-phi blank transition only when the next label is repetition
    next_phi = update_phi_score(
        next_phi, prev_emit + logprob_phi + log_epsilon * (1.0 - repeat)
    )

    pad = pad.reshape((batchsize, 1))
    next_emit = pad * prev_emit + (1.0 - pad) * next_emit
    next_phi = pad * prev_phi_orig + (1.0 - pad) * next_phi

    return (next_phi, next_emit), (next_phi, next_emit)

  xs = (logprobs_emit, logprobs_phi, logit_paddings.transpose((1, 0)))  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  _, (logalpha_phi, logalpha_emit) = jax.lax.scan(
      loop_body, (logalpha_phi_init, logalpha_emit_init), xs
  )

  # last row needs to be updated with the last epsilon transition
  logalpha_phi_last = update_phi_score(logalpha_phi[-1], logalpha_emit[-1])
  logalpha_phi = logalpha_phi.at[-1].set(logalpha_phi_last)

  # extract per_seq_loss
  one_hot = jax.nn.one_hot(labellens, num_classes=maxlabellen + 1)  # [B, N+1]
  per_seq_loss = -jnp.einsum('bn,bn->b', logalpha_phi_last, one_hot)  # pylint:disable=invalid-unary-operand-type

  return per_seq_loss, logalpha_phi, logalpha_emit

