
def use_pipelined_autotuning() -> bool:
    return (
        config.pipeline_max_autotune_gemm
        and not AutotuneProcessPool._shutdown_for_inactivity
    )

