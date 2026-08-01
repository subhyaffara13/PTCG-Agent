
def log_kernel_autotune_result(
    kernel_path: str, kernel_name: str, config: Config, latency: float
) -> None:
    get_metric_table("kernel_autotune").add_row(
        lambda: {
            "kernel_path": kernel_path,
            "kernel_name": kernel_name,
            "triton_config": str(config),
            "latency_ms": latency,
        }
    )

