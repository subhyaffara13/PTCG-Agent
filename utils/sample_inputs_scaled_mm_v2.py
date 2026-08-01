
def sample_inputs_scaled_mm_v2(op_info, device, dtype, requires_grad, **kwargs):
    from torch.nn.functional import ScalingType, SwizzleType
    make_mat_e4m3 = partial(make_tensor, device=device, dtype=torch.float8_e4m3fn, requires_grad=requires_grad)

    make_scale = partial(make_tensor, device=device, dtype=torch.float, requires_grad=False)

    M, N, K = 15, 32, 16
    samples = []
    # two e4m3 tensorwise
    mat1 = make_mat_e4m3((M, K))
    mat2 = make_mat_e4m3((K, N)).t().contiguous().t()
    scale1 = make_scale((1,))
    scale2 = make_scale((1,))
    samples.append(
        SampleInput(
            mat1,
            mat2,
            [scale1, ],
            [ScalingType.TensorWise, ],
            [SwizzleType.NO_SWIZZLE, ],
            [scale2, ],
            [ScalingType.TensorWise, ],
            [SwizzleType.NO_SWIZZLE, ],
            None,  # bias
            torch.bfloat16,  # out_dtype
        )
    )
    # two e4m3 rowwise
    mat1 = make_mat_e4m3((M, K))
    mat2 = make_mat_e4m3((K, N)).t().contiguous().t()
    scale1 = make_scale((M, 1))
    scale2 = make_scale((1, N))
    samples.append(
        SampleInput(
            mat1,
            mat2,
            [scale1, ],
            [ScalingType.RowWise, ],
            [SwizzleType.NO_SWIZZLE, ],
            [scale2, ],
            [ScalingType.RowWise, ],
            [SwizzleType.NO_SWIZZLE, ],
            None,  # bias
            torch.bfloat16,  # out_dtype
        )
    )
    M, K, N = 256, 512, 768
    mat1 = make_mat_e4m3((M, K))
    mat2 = make_mat_e4m3((K, N)).t().contiguous().t()

    if torch.device(device).type == "cuda":
        dmajor, dminor = torch.cuda.get_device_capability()

        # Blockwise scaling requires cublasLt >= 12.9 (CUDA 12.9+)
        # See: https://github.com/pytorch/pytorch/issues/172227
        cuda_version = _get_torch_cuda_version()
        if dmajor == 9 and not torch.version.hip and cuda_version >= (12, 9):
            # 1x128 x 1x128
            scale1 = make_scale((K // 128, M)).t()
            scale2 = make_scale((K // 128, N)).t()
            samples.append(
                SampleInput(
                    mat1,
                    mat2,
                    [scale1, ],
                    [ScalingType.BlockWise1x128, ],
                    [SwizzleType.NO_SWIZZLE, ],
                    [scale2, ],
                    [ScalingType.BlockWise1x128, ],
                    [SwizzleType.NO_SWIZZLE, ],
                    None,  # bias
                    torch.bfloat16,  # out_dtype
                )
            )
            # 128x128 x 1x128
            L4 = round_up(K // 128, 4)
            scale1 = make_scale((M // 128, L4)).t()
            scale2 = make_scale((K // 128, N)).t()
            samples.append(
                SampleInput(
                    mat1,
                    mat2,
                    [scale1, ],
                    [ScalingType.BlockWise128x128, ],
                    [SwizzleType.NO_SWIZZLE, ],
                    [scale2, ],
                    [ScalingType.BlockWise1x128, ],
                    [SwizzleType.NO_SWIZZLE, ],
                    None,  # bias
                    torch.bfloat16,  # out_dtype
                )
            )
            # 1x128 x 128x128
            L4 = round_up(K // 128, 4)
            scale1 = make_scale((K // 128, M)).t()
            scale2 = make_scale((N // 128, L4)).t()
            samples.append(
                SampleInput(
                    mat1,
                    mat2,
                    [scale1, ],
                    [ScalingType.BlockWise1x128, ],
                    [SwizzleType.NO_SWIZZLE, ],
                    [scale2, ],
                    [ScalingType.BlockWise128x128, ],
                    [SwizzleType.NO_SWIZZLE, ],
                    None,  # bias
                    torch.bfloat16,  # out_dtype
                )
            )

        if dmajor >= 10:
            # MXFP8
            scale1 = make_scale((M, K // 32)).to(torch.float8_e8m0fnu)
            scale2 = make_scale((K // 32, N)).to(torch.float8_e8m0fnu)
            samples.append(
                SampleInput(
                    mat1,
                    mat2,
                    [scale1, ],
                    [ScalingType.BlockWise1x32, ],
                    [SwizzleType.SWIZZLE_32_4_4, ],
                    [scale2, ],
                    [ScalingType.BlockWise1x32, ],
                    [SwizzleType.SWIZZLE_32_4_4, ],
                    None,  # bias
                    torch.bfloat16,  # out_dtype
                )
            )
            # Single-level NVFP4
            # [M, K] -> [M, K // 2]
            # [K, N] -> [K // 2, N]
            mat1_fp4 = _bfloat16_to_float4_e2m1fn_x2(mat1.to(torch.bfloat16))
            mat2_fp4 = _bfloat16_to_float4_e2m1fn_x2(mat2.to(torch.bfloat16).t()).t()
            scale1 = make_scale((M, K // 16)).to(torch.float8_e4m3fn)
            scale2 = make_scale((K // 16, N)).to(torch.float8_e4m3fn)
            samples.append(
                SampleInput(
                    mat1_fp4,
                    mat2_fp4,
                    [scale1, ],
                    [ScalingType.BlockWise1x16, ],
                    [SwizzleType.SWIZZLE_32_4_4, ],
                    [scale2, ],
                    [ScalingType.BlockWise1x16, ],
                    [SwizzleType.SWIZZLE_32_4_4, ],
                    None,  # bias
                    torch.bfloat16,  # out_dtype
                )
            )

            # NVFP4
            # [M, K] -> [M, K // 2]
            # [K, N] -> [K // 2, N]
            mat1_fp4 = _bfloat16_to_float4_e2m1fn_x2(mat1.to(torch.bfloat16))
            mat2_fp4 = _bfloat16_to_float4_e2m1fn_x2(mat2.to(torch.bfloat16).t()).t()
            scale1 = make_scale((M, K // 16)).to(torch.float8_e4m3fn)
            global_scale1 = make_scale((1, ))
            scale2 = make_scale((K // 16, N)).to(torch.float8_e4m3fn)
            global_scale2 = make_scale((1, ))
            samples.append(
                SampleInput(
                    mat1_fp4,
                    mat2_fp4,
                    [scale1, global_scale1],
                    [ScalingType.BlockWise1x16, ScalingType.TensorWise],
                    [SwizzleType.SWIZZLE_32_4_4, SwizzleType.NO_SWIZZLE],
                    [scale2, global_scale2],
                    [ScalingType.BlockWise1x16, ScalingType.TensorWise],
                    [SwizzleType.SWIZZLE_32_4_4, SwizzleType.NO_SWIZZLE],
                    None,  # bias
                    torch.bfloat16,  # out_dtype
                )
            )


    yield from samples

