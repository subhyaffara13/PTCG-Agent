
def check_is_flash_attention(
    query, key, value, layout: int, cudnn_version, has_bias, is_training,
    is_packed=False, is_paged_attention=False, is_fp8=False):
    # Extract sequence length (T) and head dim (H) based on layout
    if layout == AttentionLayout.BNTH.value:
        _, _, T, qH = query.shape
        _, _, S, vH = value.shape
    else:
        _, T, _, qH = query.shape
        _, S, _, vH = value.shape

    if is_cuda_compute_capability_equal("10.3") and cudnn_version < 91100:
      # cudnn support compute_cap 10.3 on cudnn 9.11+
      raise NotImplementedError(
        "Compute capability 10.3 requires cuDNN version >= 9.11.")

    # Flash attention conditions
    if is_fp8:
        # FP8 specific conditions
        if not ((is_training and qH == 128 and T % 128 == 0 and S % 128 == 0) or
                (not is_training and qH <= 256 and qH % 16 == 0)):
            raise NotImplementedError(
                f"Unsupported sequence length Q {T}, KV {S} and head dim {qH} for FP8."
            )
    else:
        # bf16/fp16 attention conditions
        # Check the head dim.
        is_hopper_or_later = check_compute_capability("9.0")
        H_max = 256 if is_hopper_or_later else 128
        # check if multi-head latent attention is needed
        is_mla = qH != vH
        if not (qH <= H_max and qH % 8 == 0):
          raise NotImplementedError(
              f"The head dim must be <= {H_max} and a multiple of 8, "
              f"but got {qH}."
          )

        # Check patterns with bias, seqlen should be divisible by 2
        if (is_training and has_bias and (T % 2 != 0 or S % 2 != 0)):
          raise NotImplementedError(
              f"Unsupported sequence length Q {T}, KV {S}."
          )

        if is_packed and  not check_compute_capability("9.0"):
          raise NotImplementedError(
            "Packed layout requires a GPU with at least Hopper architecture.")
        if is_mla and (cudnn_version < 91000 or not check_compute_capability("9.0")):
          raise NotImplementedError(
            "mla requires cudnn version >= 9.10 and at least hopper arch.")

