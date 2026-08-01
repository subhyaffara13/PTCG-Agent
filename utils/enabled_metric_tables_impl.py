
def enabled_metric_tables_impl(config_str: str) -> OrderedSet[str]:
    enabled: OrderedSet[str] = OrderedSet()
    for name in config_str.split(","):
        name = name.strip()
        if not name:
            continue
        assert name in REGISTERED_METRIC_TABLES, (
            f"Metric table name {name} is not registered"
        )
        enabled.add(name)
    return enabled

