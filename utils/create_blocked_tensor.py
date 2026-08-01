
def create_blocked_tensor(B, M, N, blocksize, sparsity, dtype, device):
    if sparsity < 0.0 or sparsity > 1.0:
        raise AssertionError(f"sparsity should be between 0 and 1, got {sparsity}")
    if M % blocksize[0] != 0:
        raise AssertionError(
            f"M ({M}) must be divisible by blocksize[0] ({blocksize[0]})"
        )
    if N % blocksize[1] != 0:
        raise AssertionError(
            f"N ({N}) must be divisible by blocksize[1] ({blocksize[1]})"
        )
    shape = (B, M // blocksize[0], N // blocksize[1])[int(B == 0) :]
    A = torch.bernoulli(
        torch.full(shape, 1 - sparsity, dtype=torch.float32, device=device)
    ).to(dtype)
    expected_nnz = int((1 - sparsity) * M * N / (blocksize[0] * blocksize[1]))
    nonzero_indices = A.flatten().nonzero()
    actual_nnz = nonzero_indices.shape[0]
    if actual_nnz > expected_nnz:
        selected_nonzeros = torch.randperm(actual_nnz)[: actual_nnz - expected_nnz]
        A.flatten()[nonzero_indices[selected_nonzeros]] = 0
    elif actual_nnz < expected_nnz:
        zero_indices = (A == 0).flatten().nonzero()
        selected_zeros = torch.randperm(zero_indices.shape[0])[
            : expected_nnz - actual_nnz
        ]
        A.flatten()[zero_indices[selected_zeros]] = 1
    A = torch.repeat_interleave(A, blocksize[0], dim=-2)
    A = torch.repeat_interleave(A, blocksize[1], dim=-1)
    return A

