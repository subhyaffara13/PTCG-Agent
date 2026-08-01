
def flex_attention(
    query,
    key,
    value,
    subgraph,
    block_mask,
    scale,
    kernel_options: dict[str, Any],
    score_mod_other_buffers,
    mask_mod_other_buffers,
):
    """The main lowering for the flex_attention hop
    This can currently lower to one of 3 templates:
    1. Base Triton Template
    2. Flex Decode Triton Template
    3. Cpu specific CPP template
    """
    if query.get_device().type == "cpu":
        return lower_cpu(
            query,
            key,
            value,
            subgraph,
            block_mask,
            scale,
            kernel_options,
            score_mod_other_buffers,
            mask_mod_other_buffers,
        )
    # below is cuda path if device is not cpu
    # tl.dot does not support embedding size less than 16
    small_dqk = V.graph.sizevars.evaluate_expr(sympy.Lt(query.get_size()[-1], 16))
    small_dv = V.graph.sizevars.evaluate_expr(sympy.Lt(value.get_size()[-1], 16))
    if small_dqk or small_dv:
        raise NotImplementedError(
            f"NYI: embedding dimension of the query, key, and value must be "
            f"at least 16 but got E={query.get_size()[-1]} and Ev={value.get_size()[-1]}"
        )

    (
        _,  # q_length
        _,  # kv_length
        kv_num_blocks,
        kv_indices,
        full_kv_num_blocks,
        full_kv_indices,
        q_num_blocks,
        q_indices,
        full_q_num_blocks,
        full_q_indices,
        SPARSE_Q_BLOCK_SIZE,
        SPARSE_KV_BLOCK_SIZE,
        mask_graph,
    ) = block_mask

    kernel_options, backend = _sanitize_kernel_options_for_triton(kernel_options)

    # Early check for FLASH backend: detect unsupported captured scalars before
    # building subgraph buffers (which can trigger unbacked_bindings errors)
    if backend == "FLASH":
        from .flex_flash_attention import _has_unsupported_captured_scalars

        if _has_unsupported_captured_scalars(
            score_mod_other_buffers, mask_mod_other_buffers
        ):
            raise RuntimeError(
                "BACKEND='FLASH' but flash attention cannot be used: "
                "NYI: score_mod or mask_mod captures a dynamic scalar (SymInt/SymFloat). "
                "The FLASH backend cannot inline symbolic values into the CuteDSL template. "
                "Workarounds: use BACKEND='TRITON', compile with dynamic=False, or pass the "
                "value as a tensor on device instead of capturing a Python scalar."
            )

    placeholder_inps = [
        create_placeholder(name, dtype, query.get_device())
        for name, dtype in [
            ("score", query.get_dtype()),
            ("b", torch.int32),
            ("h", torch.int32),
            ("m", torch.int32),
            ("n", torch.int32),
        ]
    ]
    subgraph_buffer = build_subgraph_buffer(
        placeholder_inps + list(score_mod_other_buffers), subgraph
    )
    freeze_irnodes(subgraph_buffer)

    mask_graph_placeholder_inps = [
        create_placeholder(name, dtype, query.get_device())
        for name, dtype in [
            ("b", torch.int32),
            ("h", torch.int32),
            ("m", torch.int32),
            ("n", torch.int32),
        ]
    ]
    mask_graph_buffer = build_subgraph_buffer(
        mask_graph_placeholder_inps + list(mask_mod_other_buffers), mask_graph
    )
    freeze_irnodes(mask_graph_buffer)
    # Mark symbols in custom kernel options as static shapes and add guards.
    kernel_options = {
        k: V.graph.sizevars.guard_int(v) if isinstance(v, sympy.Symbol) else v
        for k, v in kernel_options.items()
    }
    kernel_options.setdefault("FLOAT32_PRECISION", get_float32_precision())
    enable_gqa = V.graph.sizevars.evaluate_expr(
        sympy.Ne(query.get_size()[1], key.get_size()[1]),
    )

    can_use_decode = _use_flex_decoding(
        query, kv_indices, value, kernel_options, enable_gqa
    )
    use_decode = (backend == "TRITON_DECODE") or (backend == "AUTO" and can_use_decode)

    if backend == "TRITON_DECODE" and not can_use_decode:
        raise RuntimeError(
            "BACKEND='TRITON_DECODE' was specified but flex_decoding cannot be used for this input. "
            "flex_decoding is only available for short sequence lengths with specific configurations."
        )

    if use_decode:
        return create_flex_decoding_kernel(
            query,
            key,
            value,
            block_mask,
            scale,
            kernel_options,
            subgraph_buffer,
            mask_graph_buffer,
            score_mod_other_buffers,
            mask_mod_other_buffers,
        )

    (
        query,
        key,
        value,
        kv_num_blocks,
        kv_indices,
        full_kv_num_blocks,
        full_kv_indices,
        q_num_blocks,
        q_indices,
        full_q_num_blocks,
        full_q_indices,
    ) = maybe_realize(
        [
            query,
            key,
            value,
            kv_num_blocks,
            kv_indices,
            full_kv_num_blocks,
            full_kv_indices,
            q_num_blocks,
            q_indices,
            full_q_num_blocks,
            full_q_indices,
        ]
    )

    if _use_flex_flash_attention(
        subgraph,
        mask_graph,
        kernel_options,
        num_score_mod_placeholders=len(placeholder_inps),
        backend=backend,
    ):
        return create_flex_flash_attention_kernel(
            query,
            key,
            value,
            block_mask,
            scale,
            kernel_options,
            subgraph_buffer,
            mask_graph_buffer,
            score_mod_other_buffers,
            mask_mod_other_buffers,
            kv_num_blocks,
            kv_indices,
            full_kv_num_blocks,
            full_kv_indices,
            SPARSE_Q_BLOCK_SIZE,
            SPARSE_KV_BLOCK_SIZE,
            mask_graph=mask_graph,
            subgraph=subgraph,
        )

    score_mod_other_buffers = maybe_realize(score_mod_other_buffers)
    mask_mod_other_buffers = maybe_realize(mask_mod_other_buffers)

    freeze_irnodes(score_mod_other_buffers)
    freeze_irnodes(mask_mod_other_buffers)

    Bq, Hq, seq_len_q, qk_head_dim = query.get_size()
    Bkv, Hkv, seq_len_kv, v_head_dim = value.get_size()
    assert V.graph.sizevars.evaluate_expr(sympy.Eq(Bq, Bkv) | sympy.Eq(Bkv, 1)), (
        f"Bq and Bkv must broadcastable. Got Bq={Bq} and Bkv={Bkv}"
    )
    assert V.graph.sizevars.evaluate_expr(sympy.Gt(seq_len_q, 0)), (
        "Query length must be greater than 0"
    )
    assert V.graph.sizevars.evaluate_expr(sympy.Gt(seq_len_kv, 0)), (
        "Key length must be greater than 0"
    )

    B = Bq

    seq_q_divisible = V.graph.sizevars.statically_known_true(
        sympy.Eq(Mod(seq_len_q, 128), 0)
    )
    seq_kv_divisible = V.graph.sizevars.statically_known_true(
        sympy.Eq(Mod(seq_len_kv, 128), 0)
    )
    if seq_q_divisible and seq_kv_divisible:
        kernel_options.setdefault("IS_DIVISIBLE", True)
    else:
        kernel_options.setdefault("IS_DIVISIBLE", False)

    # NB it is okay that the v_head_dim is different
    # We are using these to match fill order of the output.
    q_strides = query.get_stride()
    # Construct output layout with strides matching the query.
    out_size = [B, Hq, seq_len_q, v_head_dim]
    out_strides = infer_dense_strides(out_size, q_strides)

    layout = FixedLayout(
        query.get_device(),
        query.get_dtype(),
        [B, Hq, seq_len_q, v_head_dim],
        stride=[sympy.sympify(s) for s in out_strides],
    )
    # see NOTE:[TritonTemplates with multiple outputs]
    logsumexp_shape = [B, Hq, seq_len_q]
    logsumexp = empty_strided(
        logsumexp_shape,
        None,
        dtype=torch.float32,  # The logsumexp is always stored in fp32 regardless of the input dtype
        device=query.get_device(),
    )
    max_scores = empty_strided(
        logsumexp_shape,  # Same shape as logsumexp
        None,
        dtype=torch.float32,  # The max scores are always stored in fp32 regardless of the input dtype
        device=query.get_device(),
    )
    kernel_options.setdefault("SM_SCALE", scale)

    # Determine GQA broadcast factor.
    gqa_shared_heads = FloorDiv(Hq, Hkv)
    kernel_options.setdefault("GQA_SHARED_HEADS", gqa_shared_heads)

    # Inside of Triton kernel, only apply partial masking if partial blocks are computed.
    # full_kv_num_blocks is None if partial blocks are not computed
    has_full_blocks = full_kv_num_blocks is not None
    kernel_options.setdefault("HAS_FULL_BLOCKS", has_full_blocks)
    if not has_full_blocks:
        full_kv_num_blocks, full_kv_indices = (
            empty(0, device=query.get_device()) for _ in range(2)
        )

    set_head_dim_values(kernel_options, qk_head_dim, v_head_dim, V.graph.sizevars)

    choices: list[Any] = []

    dtype = query.get_dtype()
    head_dim = V.graph.sizevars.guard_int(query.get_size()[-1])
    configs: list[FlexConfig] = V.choices.get_flex_attention_fwd_configs(
        head_dim, dtype, query.get_device().type
    )

    # Mark SPARSE_KV_BLOCK_SIZE & SPARSE_Q_BLOCK_SIZE as static shapes and add guards.
    SPARSE_KV_BLOCK_SIZE = V.graph.sizevars.guard_int(SPARSE_KV_BLOCK_SIZE)
    SPARSE_Q_BLOCK_SIZE = V.graph.sizevars.guard_int(SPARSE_Q_BLOCK_SIZE)

    # Note, we don't need to pass in the captured buffers explicitly
    # because they're implicitly added by the score_mod function
    # We do need to explicitly pass it in for autotuning though.
    original_kernel_options = kernel_options.copy()
    # Default config for warp specialization
    num_consumer_groups, num_buffers_warp_spec = 0, 0

    for conf in configs:
        cur_kernel_options = original_kernel_options.copy()
        # Performance tuning
        # Triton parameters
        # Remove prefix for forward kernels options and delete backward kernel options.
        for k in list(cur_kernel_options.keys()):
            if k.startswith("fwd_"):
                v = cur_kernel_options.pop(k)
                cur_kernel_options[k[4:]] = v
            if k.startswith("bwd_"):
                cur_kernel_options.pop(k)
        cur_kernel_options.setdefault("num_stages", conf.num_stages)
        cur_kernel_options.setdefault("num_warps", conf.num_warps)
        if cur_kernel_options.get("num_consumer_groups", False):
            cur_kernel_options.setdefault("num_consumer_groups", num_consumer_groups)
            cur_kernel_options.setdefault(
                "num_buffers_warp_spec", num_buffers_warp_spec
            )

        # Intel GPU enables TMA by default
        cur_kernel_options.setdefault("USE_TMA", bool(torch.xpu.is_available()))

        if cur_kernel_options["USE_TMA"] and not can_use_tma(query, key, value):
            cur_kernel_options["USE_TMA"] = False

        cur_kernel_options.setdefault("BLOCK_M", conf.block_m)
        cur_kernel_options.setdefault("BLOCK_N", conf.block_n)
        # Blocksparse options
        cur_kernel_options.setdefault("SPARSE_Q_BLOCK_SIZE", SPARSE_Q_BLOCK_SIZE)
        cur_kernel_options.setdefault("SPARSE_KV_BLOCK_SIZE", SPARSE_KV_BLOCK_SIZE)

        if (
            cur_kernel_options["SPARSE_KV_BLOCK_SIZE"] % cur_kernel_options["BLOCK_N"]
            != 0
            or cur_kernel_options["SPARSE_Q_BLOCK_SIZE"] % cur_kernel_options["BLOCK_M"]
            != 0
        ):
            if len(configs) == 1:
                raise ValueError(
                    f"Q and KV block size must be divisible by BLOCK_M and BLOCK_N. We "
                    f"got Q_BLOCK_SIZE={cur_kernel_options['SPARSE_Q_BLOCK_SIZE']} and "
                    f"KV_BLOCK_SIZE={cur_kernel_options['SPARSE_KV_BLOCK_SIZE']}."
                )
            continue

        # ROCm specific kernargs
        for attrib in ["kpack", "matrix_instr_nonkdim", "waves_per_eu"]:
            if hasattr(conf, attrib):
                cur_kernel_options[attrib] = getattr(conf, attrib)

        error = flex_attention_template.maybe_append_choice(
            choices=choices,
            input_nodes=[
                query,
                key,
                value,
                logsumexp,
                max_scores,
                kv_num_blocks,
                kv_indices,
                full_kv_num_blocks,
                full_kv_indices,
            ],
            layout=layout,
            subgraphs=[
                subgraph_buffer,
                mask_graph_buffer,
            ],
            mutated_inputs=[
                logsumexp,
                max_scores,
            ],
            call_sizes=query.get_size(),
            **cur_kernel_options,
        )
        if error is not None and len(configs) == 1:
            raise error
    inputs_for_autotuning = (
        [
            query,
            key,
            value,
            logsumexp,
            max_scores,
            kv_num_blocks,
            kv_indices,
            full_kv_num_blocks,
            full_kv_indices,
        ]
        + list(score_mod_other_buffers)
        + list(mask_mod_other_buffers)
    )
    input_gen_fns = {
        5: create_num_blocks_fake_generator(kv_indices),
        6: create_indices_fake,
        7: create_num_blocks_fake_generator(full_kv_indices),
        8: create_indices_fake,
    }

    out, _ = autotune_select_algorithm(
        "flex_attention",
        choices,
        # Need to filter out symbols since there is an invariant
        # that all input_nodes are of type IRNode
        [x for x in inputs_for_autotuning if isinstance(x, torch._inductor.ir.IRNode)],
        layout,
        input_gen_fns=input_gen_fns,
    )

    # need subgraph inputs and outputs to analyze all symints used in flex attention
    out.data.data.subgraph_inps = list(score_mod_other_buffers) + list(
        mask_mod_other_buffers
    )
    out.data.data.subgraph_outs = get_fwd_subgraph_outputs(
        subgraph_buffer, mask_graph_buffer
    )

    return (out, logsumexp, max_scores)


def flex_attention(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    score_mod: _score_mod_signature | None = ...,
    block_mask: BlockMask | None = ...,
    scale: float | None = ...,
    enable_gqa: bool = ...,
    return_lse: Literal[False] = ...,
    kernel_options: FlexKernelOptions | None = ...,
    *,
    return_aux: None = ...,
) -> Tensor: ...


def flex_attention(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    score_mod: _score_mod_signature | None = ...,
    block_mask: BlockMask | None = ...,
    scale: float | None = ...,
    enable_gqa: bool = ...,
    return_lse: Literal[True] = ...,
    kernel_options: FlexKernelOptions | None = ...,
    *,
    return_aux: None = ...,
) -> tuple[Tensor, Tensor]: ...


def flex_attention(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    score_mod: _score_mod_signature | None = ...,
    block_mask: BlockMask | None = ...,
    scale: float | None = ...,
    enable_gqa: bool = ...,
    return_lse: bool = ...,
    kernel_options: FlexKernelOptions | None = ...,
    *,
    return_aux: AuxRequest,
) -> tuple[Tensor, AuxOutput]: ...


def flex_attention(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    score_mod: _score_mod_signature | None = ...,
    block_mask: BlockMask | None = ...,
    scale: float | None = ...,
    enable_gqa: bool = ...,
    return_lse: Literal[True] = ...,
    kernel_options: FlexKernelOptions | None = ...,
    *,
    return_aux: AuxRequest,
) -> Never: ...


def flex_attention(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    score_mod: _score_mod_signature | None = None,
    block_mask: BlockMask | None = None,
    scale: float | None = None,
    enable_gqa: bool = False,
    return_lse: bool = False,
    kernel_options: FlexKernelOptions | None = None,
    *,
    return_aux: AuxRequest | None = None,
) -> Tensor | tuple[Tensor, Tensor] | tuple[Tensor, AuxOutput]:
    r"""This function implements scaled dot product attention with an arbitrary attention score modification function
    described in the `Flex Attention <https://arxiv.org/abs/2412.05496>`_ paper. See also the
    `blog post <https://pytorch.org/blog/flexattention/>`_.

    This function computes the scaled dot product attention between query, key, and value tensors with a user-defined
    attention score modification function. The attention score modification function will be applied after the attention
    scores have been calculated between the query and key tensors. The attention scores are calculated as follows:

    The ``score_mod`` function should have the following signature:

    .. code-block:: python

        def score_mod(
            score: Tensor,
            batch: Tensor,
            head: Tensor,
            q_idx: Tensor,
            k_idx: Tensor
        ) -> Tensor:

    Where:
        - ``score``: A scalar tensor representing the attention score,
          with the same data type and device as the query, key, and value tensors.
        - ``batch``, ``head``, ``q_idx``, ``k_idx``: Scalar tensors indicating
          the batch index, query head index, query index, and key/value index, respectively.
          These should have the ``torch.int`` data type and be located on the same device as the score tensor.

    Args:
        query (Tensor): Query tensor; shape :math:`(B, Hq, L, E)`. For FP8 dtypes, should be in row-major memory layout for optimal performance.
        key (Tensor): Key tensor; shape :math:`(B, Hkv, S, E)`. For FP8 dtypes, should be in row-major memory layout for optimal performance.
        value (Tensor): Value tensor; shape :math:`(B, Hkv, S, Ev)`. For FP8 dtypes, should be in column-major memory layout for optimal performance.
        score_mod (Optional[Callable]): Function to modify attention scores. By default no score_mod is applied.
        block_mask (Optional[BlockMask]): BlockMask object that controls the blocksparsity pattern of the attention.
        scale (Optional[float]): Scaling factor applied prior to softmax. If none, the default value is set to :math:`\frac{1}{\sqrt{E}}`.
        enable_gqa (bool): If set to True, enables Grouped Query Attention (GQA) and broadcasts key/value heads to query heads.
        return_lse (bool): Whether to return the logsumexp of the attention scores. Default is False. **Deprecated**: Use ``return_aux=AuxRequest(lse=True)`` instead.
        kernel_options (Optional[FlexKernelOptions]):
            Options to control the behavior of the underlying Triton kernels.
            See :class:`FlexKernelOptions` for available options and usage examples.
        return_aux (Optional[AuxRequest]): Specifies which auxiliary outputs to compute and return.
            If None, only the attention output is returned. Use ``AuxRequest(lse=True, max_scores=True)``
            to request both auxiliary outputs.

    Returns:
        output (Tensor): Attention output; shape :math:`(B, Hq, L, Ev)`.

        When ``return_aux`` is not None:
            aux (AuxOutput): Auxiliary outputs with requested fields populated.

        When ``return_aux`` is None (deprecated paths):
            lse (Tensor): Log-sum-exp of attention scores; shape :math:`(B, Hq, L)`. Only returned if ``return_lse=True``.

    Shape legend:
        - :math:`N: \text{Batch size} ... : \text{Any number of other batch dimensions (optional)}`
        - :math:`S: \text{Source sequence length}`
        - :math:`L: \text{Target sequence length}`
        - :math:`E: \text{Embedding dimension of the query and key}`
        - :math:`Ev: \text{Embedding dimension of the value}`

    .. warning::
        `torch.nn.attention.flex_attention` is a prototype feature in PyTorch.
        Please look forward to a more stable implementation in a future version of PyTorch.
        Read more about feature classification at: https://pytorch.org/blog/pytorch-feature-classification-changes/#prototype

    """
    # Some basic input validation
    _validate_sdpa_input(query, key, value, allow_lowp_kv=True)
    _validate_embed_dim(query, key, value)
    _validate_device(query, key, value)
    query, key, value = _enforce_mem_layouts(query, key, value)
    if query.dim() != 4 or key.dim() != 4 or value.dim() != 4:
        raise NotImplementedError("NYI: query, key, and value must be 4D tensors")
    if (not enable_gqa) and query.size(-3) != key.size(-3):
        raise ValueError(
            f"Expect query and key/value to have the same number of heads "
            f"but got Hq={query.size(-3)} and Hkv={key.size(-3)}. "
            f"Try setting enable_gqa=True for GQA."
        )
    if enable_gqa:
        Hq = query.size(1)
        Hkv = key.size(1)
        if Hq % Hkv != 0:
            raise ValueError(
                f"Expect number of query heads to be a multiple of kv heads for GQA "
                f"but got Hq={Hq} and Hkv={Hkv}."
            )
    if query.size(0) != key.size(0):
        if block_mask is None:
            raise ValueError(
                f"Expect query and key/value to have the same batch size, "
                f"or non-none block_mask, "
                f"but got block_mask=None, Bq={query.size(0)}, and Bkv={key.size(0)}."
            )

        if block_mask.kv_num_blocks.size(0) != query.size(0):
            raise ValueError(
                f"Expect query and key/value to have the same batch size, "
                f"or block_mask and query to have the same batch size, "
                f"but got Bq={query.size(0)}, Bkv={key.size(0)}, B_block_mask={block_mask.kv_num_blocks.size(0)}."
            )

    if score_mod is None:
        score_mod = _identity

    if block_mask is None:
        block_mask = _create_empty_block_mask(query, key)

    # If BlockMask was sliced, its mask_mod is intentionally replaced with an error-raising stub.
    # This guard ensures we surface the intended error message before any shape-based checks.
    if getattr(block_mask, "mask_mod", None) is _sliced_mask_mod_error:
        raise RuntimeError("Cannot use mask_mod from a sliced BlockMask")

    if (
        block_mask.BLOCK_SIZE[0] == _LARGE_SPARSE_BLOCK_SIZE
        and block_mask.BLOCK_SIZE[1] == _LARGE_SPARSE_BLOCK_SIZE
    ):
        # This corresponds to the case where we essentially have a "no-op" block mask.
        pass
    else:
        block_mask_q_len = block_mask.shape[-2]
        block_mask_kv_len = block_mask.shape[-1]
        if query.size(-2) > block_mask_q_len or key.size(-2) > block_mask_kv_len:
            raise ValueError(
                f"block_mask was created for block_mask.shape={block_mask.shape} but got q_len={query.size(-2)} and kv_len={key.size(-2)}. "
                "As the block mask was created for a smaller length than you're using it for, you likely need to create a new block mask."
            )
        elif (
            query.size(-2) < block_mask_q_len and key.size(-2) <= block_mask_kv_len
        ) or (query.size(-2) <= block_mask_q_len and key.size(-2) < block_mask_kv_len):
            raise ValueError(
                f"block_mask was created for block_mask.shape={block_mask.shape} but got q_len={query.size(-2)} and kv_len={key.size(-2)}. "
                "As the block mask was created for a larger length than you're using it for, you can either 1. create a new block mask with the correct length, or 2. 'adjust' the existing block mask to the correct length by calling block_mask._adjust(q_len, kv_len). This essentially 'crops' the block mask to the upper left corner, which does not work for all mask_mods!"
            )
        if query.size(-2) != block_mask_q_len:
            raise AssertionError(
                f"query.size(-2) ({query.size(-2)}) != block_mask_q_len ({block_mask_q_len})"
            )
        if key.size(-2) != block_mask_kv_len:
            raise AssertionError(
                f"key.size(-2) ({key.size(-2)}) != block_mask_kv_len ({block_mask_kv_len})"
            )

    if scale is None:
        scale = 1.0 / math.sqrt(query.size(-1))

    if query.device != block_mask.kv_num_blocks.device:  # type: ignore[union-attr]
        raise RuntimeError(
            f"Expect q/k/v and block_mask to be on the same device "
            f"but got {query.device} and {block_mask.kv_num_blocks.device}."  # type: ignore[union-attr]
        )

    # Handle deprecation warnings for old parameters
    if return_lse and return_aux is not None:
        raise ValueError(
            "Cannot specify both return_lse and return_aux. "
            "return_lse is deprecated, please use return_aux=AuxRequest(lse=True) instead."
        )
    elif return_lse and return_aux is None:
        _warn_once(
            "deprecated_return_lse",
            "return_lse is deprecated and will be removed in v2.10. "
            "Please use return_aux=AuxRequest(lse=True) instead.",
            category=FutureWarning,
        )

    kernel_options = _apply_kernel_options(
        query,
        key,
        value,
        return_lse,
        kernel_options,
        return_aux,
    )

    def _finalize_outputs(
        out,
        lse,
        max_scores,
        *,
        return_aux: AuxRequest | None,
        return_lse: bool,
    ):
        """Normalize stats and build return value (aux-aware, legacy-compatible)."""
        ln2 = math.log(2.0)
        return_lse = return_lse or return_aux is not None and return_aux.lse
        return_max = return_aux is not None and return_aux.max_scores

        lse_scaled = lse * ln2 if (return_lse and lse.numel() > 0) else None
        max_scaled = (
            max_scores * ln2 if (return_max and max_scores.numel() > 0) else None
        )

        if return_aux is not None:
            return out, AuxOutput(
                lse=lse_scaled,
                max_scores=max_scaled,
            )

        if return_lse:
            return out, lse_scaled

        return out

    if torch.compiler.is_dynamo_compiling():
        # mark head_dim and number of heads to be static
        for x in [query, key, value]:
            torch._dynamo.mark_static(x, -3)
            torch._dynamo.mark_static(x, -1)

        out, lse, max_scores = flex_attention_hop(
            query,
            key,
            value,
            score_mod,
            block_mask.as_tuple(),
            scale,
            kernel_options,  # type: ignore[union-attr]
        )
        return _finalize_outputs(
            out, lse, max_scores, return_aux=return_aux, return_lse=return_lse
        )

    if not _FLEX_ATTENTION_DISABLE_COMPILE_DEBUG:
        _warn_once(
            warning_id="flex_attention_performance",
            message=(
                "flex_attention called without torch.compile() - this will use an unfused implementation that materializes the full scores matrix instead of generating a fused kernel.\n\n"
                "SOLUTION: Use torch.compile(flex_attention)(...)\n\n"
                "If you want to debug your score_mod/mask_mod, you can set:\n"
                "torch.nn.attention.flex_attention._FLEX_ATTENTION_DISABLE_COMPILE_DEBUG = True\n\n"
                "This will allow you to use print statements or breakpoints. Note: This doesn't work with the backwards pass and may produce incorrect results."
            ),
        )

    if not torch._dynamo.is_dynamo_supported():
        raise RuntimeError("flex_attention requires dynamo support")

    # Dynamo is expecting a callable with "__code__" attribute.
    # We cannot directly pass hop to it. So we wrap it in a dummy function.
    def _flex_attention_hop_wrapper(*args, **kwargs):
        return flex_attention_hop(*args, **kwargs)

    with setup_compilation_env() as backend:
        if _FLEX_ATTENTION_DISABLE_COMPILE_DEBUG:
            flex_fn = _flex_attention_hop_wrapper
        else:
            flex_fn = torch.compile(
                _flex_attention_hop_wrapper, backend=backend, fullgraph=True
            )

        out, lse, max_scores = flex_fn(
            query,
            key,
            value,
            score_mod,
            block_mask.as_tuple(),
            scale,
            kernel_options,
        )
    return _finalize_outputs(
        out, lse, max_scores, return_aux=return_aux, return_lse=return_lse
    )

