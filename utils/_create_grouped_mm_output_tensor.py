
def _create_grouped_mm_output_tensor(mat1, mat2, offs, out_dtype):
    mat1_is_2d = mat1.dim() == 2
    mat2_is_2d = mat2.dim() == 2

    if mat1_is_2d:
        if mat2_is_2d:
            out_size = [offs.size(0), mat1.size(0), mat2.size(1)]
        else:
            torch._check(
                offs.size(0) == mat2.size(0), lambda: "matrix batch sizes have to match"
            )
            out_size = [mat1.size(0), mat2.size(-1)]
    else:
        if mat2_is_2d:
            torch._check(
                offs.size(0) == mat1.size(0), lambda: "matrix batch sizes have to match"
            )
            out_size = [mat1.size(1), mat2.size(1)]
        else:
            # regular bmm
            torch._check(
                mat1.size(0) == mat2.size(0), lambda: "batched dimension has to match"
            )
            out_size = [mat1.size(0), mat1.size(1), mat2.size(-1)]

    out_dtype = out_dtype or mat1.dtype

    if torch.version.cuda:
        alignment = 16 // out_dtype.itemsize
        size_padded = (out_size[-1] + alignment - 1) // alignment * alignment
        if mat1_is_2d == mat2_is_2d:
            out_stride = [out_size[1] * size_padded, size_padded, 1]
        else:
            out_stride = [size_padded, 1]
        out = torch.empty_strided(
            out_size, out_stride, dtype=out_dtype, device=mat1.device
        )
    else:
        out = torch.empty(out_size, dtype=out_dtype, device=mat1.device)
    return out

