
def _calculate_meta_reordering_scatter_offsets(m, meta_ncols, meta_dtype, device):
    """
    This is PyTorch implementation of main part of reorder_meta()
    function, from tools/util/include/cutlass/util/host_reorder.h file
    of CUTLASS source tree.  Furthermore, CUTLASS template for sparse
    GEMM decides upon layout of this matrix, and at the moment for the
    sparse GEMM executed on tensor cores, this is layout described by
    ColumnMajorInterleaved<2> data structure, in
    include/cutlass/layout/matrix.h of CUTLASS source tree.  The
    reordering of meta matrix into meta_reordered matrix calculated
    according to these segments of CUTLASS code is re-implemented here.
    Note that this calculation produces offsets for scattering metadata
    matrix elements into reordered metadata matrix elements (or,
    equivalently, for gathering reordered metadata matrix element back
    into metadata matrix elements).
    """
    dst_rows = torch.arange(0, m, device=device)[:, None].repeat(1, meta_ncols)
    dst_cols = torch.arange(0, meta_ncols, device=device).repeat(m, 1)

    # Reorder the rows, then swizzle the 2x2 blocks.
    group = 32 if meta_dtype.itemsize == 2 else 16
    interweave = 4 if meta_dtype.itemsize == 2 else 2
    dst_rows = (
        dst_rows // group * group
        + (dst_rows % 8) * interweave
        + (dst_rows % group) // 8
    )

    topright = ((dst_rows % 2 == 0) & (dst_cols % 2 == 1)).to(torch.int8)
    bottomleft = ((dst_rows % 2 == 1) & (dst_cols % 2 == 0)).to(torch.int8)
    dst_rows += topright - bottomleft
    dst_cols -= topright - bottomleft

    # Assumed that meta tensor is to be stored in CUTLASS
    # InterleavedColumnMajor layout, and reverse engineered
    # corresponding code to store values into this tensor.
    interleave = 2
    cols_maj = dst_cols // interleave
    cols_min = dst_cols % interleave
    return (cols_maj * m * interleave + dst_rows * interleave + cols_min).view(-1)

