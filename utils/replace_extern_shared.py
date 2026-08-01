
def replace_extern_shared(input_string):
    """
    Match 'extern __shared__ type foo[];' syntax and use HIP_DYNAMIC_SHARED() MACRO instead.
    See: https://github.com/ROCm/hip/blob/master/docs/markdown/hip_kernel_language.md#__shared__
    Examples:
        "extern __shared__ char smemChar[];"
            => "HIP_DYNAMIC_SHARED( char, smemChar)"
        "extern __shared__ unsigned char smem[];"
            => "HIP_DYNAMIC_SHARED( unsigned char, my_smem)"
    """
    output_string = input_string
    output_string = RE_EXTERN_SHARED.sub(
        lambda inp: f"HIP_DYNAMIC_SHARED({inp.group(1) or ''} {inp.group(2)}, {inp.group(3)})", output_string)

    return output_string

