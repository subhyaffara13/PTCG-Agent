
def enabled_metric_tables() -> OrderedSet[str]:
    return enabled_metric_tables_impl(config.enabled_metric_tables)

