
def _b_orthonormalize(B, blockVectorV, blockVectorBV=None,
                      verbosityLevel=0):
    """in-place B-orthonormalize the given block vector using Cholesky."""
    if blockVectorBV is None:
        if B is None:
            blockVectorBV = blockVectorV
        else:
            try:
                blockVectorBV = B(blockVectorV)
            except Exception as e:
                if verbosityLevel:
                    warnings.warn(
                        f"Secondary MatMul call failed with error\n"
                        f"{e}\n",
                        UserWarning, stacklevel=3
                    )
                    return None, None, None
            if blockVectorBV.shape != blockVectorV.shape:
                raise ValueError(
                    f"The shape {blockVectorV.shape} "
                    f"of the orthogonalized matrix not preserved\n"
                    f"and changed to {blockVectorBV.shape} "
                    f"after multiplying by the secondary matrix.\n"
                )

    VBV = blockVectorV.T.conj() @ blockVectorBV
    try:
        # VBV is a Cholesky factor from now on...
        VBV = cholesky(VBV, overwrite_a=True)
        VBV = inv(VBV, overwrite_a=True)
        blockVectorV = _matmul_inplace(
            blockVectorV, VBV,
            verbosityLevel=verbosityLevel
        )
        if B is not None:
            blockVectorBV = _matmul_inplace(
                blockVectorBV, VBV,
                verbosityLevel=verbosityLevel
            )
        return blockVectorV, blockVectorBV, VBV
    except LinAlgError:
        if verbosityLevel:
            warnings.warn(
                "Cholesky has failed.",
                UserWarning, stacklevel=3
            )
        return None, None, None

