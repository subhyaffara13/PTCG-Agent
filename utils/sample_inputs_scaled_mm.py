
def sample_inputs_scaled_mm(op_info, device, dtype, requires_grad, **kwargs):
    def to_fp8_saturated(x: torch.Tensor, fp8_dtype: torch.dtype) -> torch.Tensor:
        max_val = E4M3_MAX_POS if fp8_dtype == e4m3_type else E5M2_MAX_POS
        x = x.clamp(min=-1 * max_val, max=max_val)
        return x.to(fp8_dtype)

    def amax_to_scale(amax: torch.Tensor, float8_dtype: torch.dtype) -> torch.Tensor:
        EPS = 1e-12
        max_pos = E4M3_MAX_POS if float8_dtype == e4m3_type else E5M2_MAX_POS
        scale_val = max_pos / torch.clamp(amax, min=EPS)
        return scale_val.to(dtype=torch.float32, device=device)

    def make_scale(x: float, float8_dtype: torch.dtype, dim=None) -> torch.Tensor:
        if dim is None:
            amax = torch.tensor(abs(x), dtype=torch.float32, device=device)
        else:
            amax = torch.max(
                torch.abs(torch.tensor(x, device=device)), dim=dim, keepdim=True
            ).values
        return amax_to_scale(amax, float8_dtype)

    def make_mat(size: tuple[int], scale: float, fp8_dtype: torch.dtype) -> torch.Tensor:
        mat = torch.randn(size, device=device, dtype=torch.float32)
        return to_fp8_saturated(mat * scale, fp8_dtype)

    M, N, K = 15, 32, 16
    samples = []

    # Case 1: Both matrices e4m3
    scale1 = random.random()
    scale2 = random.random()
    mat1 = make_mat((M, K), scale1, torch.float8_e4m3fn)
    mat2 = make_mat((K, N), scale2, torch.float8_e4m3fn).t().contiguous().t()
    scale_tensor1 = make_scale(scale1, torch.float8_e4m3fn)
    scale_tensor2 = make_scale(scale2, torch.float8_e4m3fn)
    samples.append(SampleInput(mat1, mat2, scale_tensor1, scale_tensor2))

    # Case 2: mat1 e4m3, mat2 e5m2
    scale1 = random.random()
    scale2 = random.random()
    mat1 = make_mat((M, K), scale1, torch.float8_e4m3fn)
    mat2 = make_mat((K, N), scale2, torch.float8_e5m2).t().contiguous().t()
    scale_tensor1 = make_scale(scale1, torch.float8_e4m3fn)
    scale_tensor2 = make_scale(scale2, torch.float8_e5m2)
    samples.append(SampleInput(mat1, mat2, scale_tensor1, scale_tensor2))

    # Case 3: mat1 e5m2, mat2 e4m3
    scale1 = random.random()
    scale2 = random.random()
    mat1 = make_mat((M, K), scale1, torch.float8_e5m2)
    mat2 = make_mat((K, N), scale2, torch.float8_e4m3fn).t().contiguous().t()
    scale_tensor1 = make_scale(scale1, torch.float8_e5m2)
    scale_tensor2 = make_scale(scale2, torch.float8_e4m3fn)
    samples.append(SampleInput(mat1, mat2, scale_tensor1, scale_tensor2))

    # Case 4: MXFP4 (float4_e2m1fn_x2) with E8M0 blockwise scaling
    # Regression test: E8M0 blockwise scale size validation must account for
    # packed FP4 format where self.size(1) = K/2.
    # Only supported on MI350 (gfx950).
    if device == 'cuda' and torch.version.hip:
        if 'gfx950' in torch.cuda.get_device_properties(0).gcnArchName:
            mxfp4_M, mxfp4_K, mxfp4_N = 256, 256, 256
            block_size_k = 32
            block_size_mn = 128
            num_k_blocks = math.ceil(mxfp4_K / block_size_k)
            padded_num_k_blocks = math.ceil(num_k_blocks / 4) * 4
            scale_a_size = block_size_mn * math.ceil(mxfp4_M / block_size_mn) * padded_num_k_blocks
            scale_b_size = block_size_mn * math.ceil(mxfp4_N / block_size_mn) * padded_num_k_blocks
            mat1 = _bfloat16_to_float4_e2m1fn_x2(
                torch.randn(mxfp4_M, mxfp4_K, device=device, dtype=torch.bfloat16)
            )
            mat2 = _bfloat16_to_float4_e2m1fn_x2(
                torch.randn(mxfp4_N, mxfp4_K, device=device, dtype=torch.bfloat16)
            ).t()
            scale_tensor1 = torch.ones(scale_a_size, device=device, dtype=torch.float8_e8m0fnu)
            scale_tensor2 = torch.ones(scale_b_size, device=device, dtype=torch.float8_e8m0fnu)
            samples.append(SampleInput(
                mat1, mat2, scale_tensor1, scale_tensor2,
                out_dtype=torch.bfloat16,
            ))

    yield from samples

