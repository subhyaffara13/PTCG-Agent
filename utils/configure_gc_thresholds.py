
def configure_gc_thresholds():
    """Configure Python garbage collection thresholds from environment variables."""
    gc_threshold_env = PYTHON_GC_THRESHOLD
    if gc_threshold_env:
        try:
            # Parse threshold string like "1000,50,50"
            thresholds = [int(x.strip()) for x in gc_threshold_env.split(",")]
            if len(thresholds) == 3:
                gc.set_threshold(*thresholds)
                verbose_proxy_logger.info(f"GC thresholds set to: {thresholds}")
            else:
                verbose_proxy_logger.warning(
                    f"GC threshold not set: {gc_threshold_env}. Expected format: 'gen0,gen1,gen2'"
                )
        except ValueError as e:
            verbose_proxy_logger.warning(
                f"Failed to parse GC threshold: {gc_threshold_env}. Error: {e}"
            )

    # Log current thresholds
    current_thresholds = gc.get_threshold()
    verbose_proxy_logger.info(
        f"Current GC thresholds: gen0={current_thresholds[0]}, gen1={current_thresholds[1]}, gen2={current_thresholds[2]}"
    )

