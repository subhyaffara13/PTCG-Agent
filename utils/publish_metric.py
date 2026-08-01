
def publish_metric(metric_group: str, metric_name: str, metric_value: int):
    metric_stream = getStream(metric_group)
    metric_stream.add_value(metric_name, metric_value)

