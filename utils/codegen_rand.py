
def codegen_rand(offset, code, rand_function, dst_dtype=torch.float32):
    assert is_integer_dtype(offset.dtype)
    code.writeline("[&]()")
    with code.indent():
        code.writeline(
            f"{DTYPE_TO_CPP[offset.dtype]} offset[{V.kernel.tiling_factor}];"
        )
        code.writeline(f"{DTYPE_TO_CPP[dst_dtype]} result[{V.kernel.tiling_factor}];")
        code.writeline(f"{offset}.store(offset);")
        code.writeline(
            f"for( {DTYPE_TO_CPP[offset.dtype]} offset_idx = 0; offset_idx < {V.kernel.tiling_factor}; offset_idx++ )"
        )
        with code.indent():
            code.writeline(rand_function)
        num_vectors = V.kernel._get_num_vectors(dtype=dst_dtype)
        if num_vectors == 1:
            code.writeline(
                f"return at::vec::Vectorized<{DTYPE_TO_CPP[dst_dtype]}>::loadu(result);"
            )
        else:
            code.writeline(
                f"return at::vec::VectorizedN<{DTYPE_TO_CPP[dst_dtype]}, {num_vectors}>::loadu(result);"
            )
    code.writeline("()")
    return code

