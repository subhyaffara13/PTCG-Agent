
def register_micro_gemm(*configs):
    def inner(cls):
        assert cls not in micro_gemm_configs, (
            f"Duplicate micro_gemm registration for {cls}"
        )
        assert len(configs) > 0, f"No micro_gemm configs provided for {cls}"
        micro_gemm_configs[cls] = list(configs)
        return cls

    return inner

