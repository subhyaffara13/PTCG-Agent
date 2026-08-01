
def make_attention_reference(
    mask: mask_lib.Mask | np.ndarray,
    is_mqa: bool,
    backward_impl: str = "vanilla",
    **params: Any,
) -> Callable:
  @partial(
      jax.jit,
      static_argnames=[
          "mask_value",
          "save_residuals",
          "attn_logits_soft_cap",
      ],
  )
  def _wrapped(
      mask: jax.Array,
      q: jax.Array,
      k: jax.Array,
      v: jax.Array,
      segment_ids: SegmentIds | None = None,
      sinks: jax.Array | None = None,
      *,
      mask_value: float = DEFAULT_MASK_VALUE,
      save_residuals: bool = False,
      attn_logits_soft_cap: float | None = None,
  ):
    if backward_impl == "custom":
      attn_impl = partial(
          attention_reference_custom, custom_type="flash",
      )
    elif backward_impl == "custom_vanilla":
      attn_impl = partial(
          attention_reference_custom, custom_type="vanilla",
      )
    else:
      attn_impl = attention_reference
    func = partial(
        attn_impl,
        mask_value=mask_value,
        save_residuals=save_residuals,
        attn_logits_soft_cap=attn_logits_soft_cap,
        **params,
    )

    if is_mqa:
      func = jax.vmap(func, in_axes=(0, 0, None, None, None, 0))
      is_grouped = False
    else:
      # In grouped attention (1 < num_kv_heads && num_kv_heads < num_q_heads).
      # We interleave the KV heads across the Q heads.
      # For example: for 8 Q heads and 4 KV heads:
      # Q head [0, 1] see KV head 0
      # Q head [2, 3] see KV head 1
      # Q head [4, 5] see KV head 2
      # Q head [6, 7] see KV head 3
      #
      # The following implementation reshapes Q to expose KV heads and vmaps
      # Across the Q heads so it is similar to MQA.
      # Alternatively we can replicate K/V to match Q like so:
      # k = jnp.repeat(k, q_heads_per_kv_head, axis=0)
      # v = jnp.repeat(v, q_heads_per_kv_head, axis=0)

      kv_heads = k.shape[0]
      assert kv_heads == v.shape[0]
      q_heads, q_seq_len, head_dim = q.shape
      is_grouped = kv_heads < q_heads
      if is_grouped:
        assert q_heads % kv_heads == 0
        assert mask.shape[0] == q_heads
        q_heads_per_kv_head = q_heads // kv_heads
        q = q.reshape((kv_heads, q_heads_per_kv_head, q_seq_len, head_dim))
        mask = mask.reshape((kv_heads, q_heads_per_kv_head, *mask.shape[1:]))
        if sinks is not None:
          sinks = sinks.reshape((kv_heads, q_heads_per_kv_head))

        # Inner-most vmap: iterate over the q heads.
        func = jax.vmap(func, in_axes=(0, 0, None, None, None, 0))

      # Outer-most vmap: iterate over the kv heads.
      func = jax.vmap(func, in_axes=(0, 0, 0, 0, None, 0))

    out = func(mask, q, k, v, segment_ids, sinks)

    if is_grouped:

      def reshape_activations(activations):
        if activations.ndim == 4:
          kv_heads, q_heads_per_kv_head, q_seq_len, head_dim = activations.shape
          return activations.reshape(
              kv_heads * q_heads_per_kv_head, q_seq_len, head_dim
          )
        return activations

      def reshape_residuals(residuals):
        if residuals.ndim == 3:
          kv_heads, q_heads_per_kv_head, q_seq_len = residuals.shape
          return residuals.reshape(kv_heads * q_heads_per_kv_head, q_seq_len)
        return residuals

      if save_residuals:
        assert isinstance(out, tuple)
        assert isinstance(out[1], tuple)

        return (reshape_activations(out[0]), (reshape_residuals(out[1][0]),))
      else:
        return reshape_activations(out)
    else:
      return out

  return functools.partial(_wrapped, jnp.array(mask[:, :, :]))

