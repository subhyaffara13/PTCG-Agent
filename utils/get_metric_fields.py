
def get_metric_fields() -> list[str]:
    return [field.name for field in dataclasses.fields(CachedMetricsDeltas)]

