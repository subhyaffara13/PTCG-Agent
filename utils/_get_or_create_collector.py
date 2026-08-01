
def _get_or_create_collector() -> Optional[RedisMetricsCollector]:
    """
    Get or create the global metrics collector.

    Returns:
        RedisMetricsCollector instance if observability is enabled, None otherwise
    """
    try:
        manager = get_observability_instance().get_provider_manager()
        if manager is None or not manager.config.enabled_telemetry:
            return None

        # Get meter from the global MeterProvider
        meter = manager.get_meter_provider().get_meter(
            RedisMetricsCollector.METER_NAME, RedisMetricsCollector.METER_VERSION
        )

        return RedisMetricsCollector(meter, manager.config)

    except ImportError:
        # Observability module not available
        return None
    except Exception:
        # Any other error - don't break Redis operations
        return None


def _get_or_create_collector() -> Optional[RedisMetricsCollector]:
    """
    Get or create the global metrics collector.

    Returns:
        RedisMetricsCollector instance if observability is enabled, None otherwise
    """
    global _async_metrics_collector

    if _async_metrics_collector is not None:
        return _async_metrics_collector

    try:
        manager = get_observability_instance().get_provider_manager()
        if manager is None or not manager.config.enabled_telemetry:
            return None

        # Get meter from the global MeterProvider
        meter = manager.get_meter_provider().get_meter(
            RedisMetricsCollector.METER_NAME, RedisMetricsCollector.METER_VERSION
        )

        _async_metrics_collector = RedisMetricsCollector(meter, manager.config)
        return _async_metrics_collector

    except ImportError:
        # Observability module not available
        return None
    except Exception:
        # Any other error - don't break Redis operations
        return None

