
def _use_template_for_cpu(layout: Layout) -> bool:
    return (
        config.max_autotune or config.max_autotune_gemm
    ) and layout.device.type == "cpu"

