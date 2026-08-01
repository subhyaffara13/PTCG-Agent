
def get_kai_packed_weight_size(n_bits, N, K, groupsize):
    if n_bits == 4:
        # Works for both fp32 and bf16 Kernels
        if groupsize == K:  # channelwise
            # dotprod params only [1x8x32_neon_dotprod]
            kai_nr = 8
            kai_kr = 16
            kai_sr = 2
            kai_num_bytes_sum_rhs = 4  # sizeof(int32_t)
            kai_num_bytes_multiplier_rhs = 4  # sizeof(float)
            kai_num_bytes_bias = 4  # sizeof(float)

            def kai_k_roundedup(k, kr, sr):
                # Since we pack a float and int32 value at the end of the row,
                # we must make sure that k is a multiple of 4 for alignment
                kr_sr_roundedup4 = kai_roundup(kr * sr, 4)
                return kai_roundup(k, kr_sr_roundedup4)

            def kai_get_rhs_packed_stride_rhs_pack_nxk_qsi4cxp_qsu4cxs1s0(
                k, nr, kr, sr
            ):
                k_internal = kai_k_roundedup(k, kr, sr)

                if (k_internal % 2) != 0:
                    raise AssertionError(f"k_internal must be even, got {k_internal}")

                return nr * (
                    (k_internal // 2)
                    + kai_num_bytes_multiplier_rhs
                    + kai_num_bytes_sum_rhs
                    + kai_num_bytes_bias
                )

            def kai_get_rhs_packed_size_rhs_pack_nxk_qsi4cxp_qsu4cxs1s0(
                n, k, nr, kr, sr
            ):
                num_rows = kai_roundup(n, nr) // nr

                return (
                    num_rows
                    * kai_get_rhs_packed_stride_rhs_pack_nxk_qsi4cxp_qsu4cxs1s0(
                        k, nr, kr, sr
                    )
                )

            return kai_get_rhs_packed_size_rhs_pack_nxk_qsi4cxp_qsu4cxs1s0(
                N, K, kai_nr, kai_kr, kai_sr
            )
        elif groupsize % 32 == 0 and K % groupsize == 0:  # groupwise
            kai_nr = 8
            kai_kr = 16
            kai_sr = 2
            kai_num_bytes_sum_rhs = 4
            kai_num_bytes_bias = 4
            kai_nr_multiple_of = 4
            kai_bl_multiple_of = 32

            def kai_get_rhs_packed_size_rhs_pack_nxk_qsi4c32p_qsu4c32s1s0(
                n, k, nr, kr, sr, bl
            ):
                if (bl % kr) != 0:
                    raise AssertionError(f"bl ({bl}) must be divisible by kr ({kr})")
                if (nr % kai_nr_multiple_of) != 0:
                    raise AssertionError(
                        f"nr ({nr}) must be divisible by kai_nr_multiple_of ({kai_nr_multiple_of})"
                    )
                if (bl % kai_bl_multiple_of) != 0:
                    raise AssertionError(
                        f"bl ({bl}) must be divisible by kai_bl_multiple_of ({kai_bl_multiple_of})"
                    )

                num_rows = kai_roundup(n, nr) // nr

                return (
                    num_rows
                    * kai_get_rhs_packed_stride_rhs_pack_nxk_qsi4c32p_qsu4c32s1s0(
                        k, nr, kr, sr, bl
                    )
                )

            def kai_get_rhs_packed_stride_rhs_pack_nxk_qsi4c32p_qsu4c32s1s0(
                k, nr, kr, sr, bl
            ):
                if (bl % kr) != 0:
                    raise AssertionError(f"bl ({bl}) must be divisible by kr ({kr})")
                if (nr % kai_nr_multiple_of) != 0:
                    raise AssertionError(
                        f"nr ({nr}) must be divisible by kai_nr_multiple_of ({kai_nr_multiple_of})"
                    )
                if (bl % kai_bl_multiple_of) != 0:
                    raise AssertionError(
                        f"bl ({bl}) must be divisible by kai_bl_multiple_of ({kai_bl_multiple_of})"
                    )

                # kr and sr are unused in the calculation
                num_bytes_multiplier_rhs = kai_get_bf16_datatype_size_in_bytes()
                num_blocks_per_row = kai_num_blocks_per_row(k, bl)
                num_bytes_per_block = kai_num_bytes_per_block(
                    bl, num_bytes_multiplier_rhs
                )

                return nr * (
                    (num_bytes_per_block * num_blocks_per_row)
                    + kai_num_bytes_sum_rhs
                    + kai_num_bytes_bias
                )

            # This function returns size of these datatypes stored as enum. We modify it to just return bf16 datatype
            # https://gitlab.arm.com/kleidi/kleidiai/-/blob/main/kai/kai_common.h?ref_type=heads#L55
            def kai_get_bf16_datatype_size_in_bytes():
                return 2  # 2 bytes

            def kai_num_blocks_per_row(k, bl):
                if (bl % kai_bl_multiple_of) != 0:
                    raise AssertionError(
                        f"bl ({bl}) must be divisible by kai_bl_multiple_of ({kai_bl_multiple_of})"
                    )
                return kai_roundup(k, bl) // bl

            def kai_num_bytes_per_block(bl, num_bytes_multiplier_rhs):
                if (bl % kai_bl_multiple_of) != 0:
                    raise AssertionError(
                        f"bl ({bl}) must be divisible by kai_bl_multiple_of ({kai_bl_multiple_of})"
                    )
                return (bl // 2) + num_bytes_multiplier_rhs

            return kai_get_rhs_packed_size_rhs_pack_nxk_qsi4c32p_qsu4c32s1s0(
                N, K, kai_nr, kai_kr, kai_sr, groupsize
            )

