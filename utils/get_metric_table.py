
def get_metric_table(name: str) -> MetricTable:
    assert name in REGISTERED_METRIC_TABLES, f"Metric table {name} is not defined"
    return REGISTERED_METRIC_TABLES[name]

