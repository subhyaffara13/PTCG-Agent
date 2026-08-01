
def get_isa_from_cpu_capability(
    capability: str | None,
    vec_isa_list: list[VecISA],
    invalid_vec_isa: InvalidVecISA,
):
    # AMX setting is not supported in eager
    # VecAMX will be prioritized for selection when setting ATEN_CPU_CAPABILITY to avx512
    # TODO add sve256 support
    capability_to_isa_str = {
        "default": "INVALID_VEC_ISA",
        "zvector": "zvector",
        "vsx": "vsx",
        "avx2": "avx2",
        "avx512": "avx512",
    }
    if capability in capability_to_isa_str:
        # pyrefly: ignore [bad-index, index-error]
        isa_str = capability_to_isa_str[capability]
        if isa_str == "INVALID_VEC_ISA":
            return invalid_vec_isa
        for vec_isa in vec_isa_list:
            if isa_str in str(vec_isa):
                return vec_isa

    if capability:
        warnings.warn(f"ignoring invalid value for ATEN_CPU_CAPABILITY {capability}")

    return vec_isa_list[0]

