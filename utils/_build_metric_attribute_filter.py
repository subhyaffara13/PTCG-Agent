from typing import Any

def _build_metric_attribute_filter(value: Any) -> OTELMetricAttributeFilter:
    if isinstance(value, OTELMetricAttributeFilter):
        return value
    if not isinstance(value, dict):
        raise ValueError(
            "otel.attributes must be a mapping with optional 'include_list' / "
            f"'exclude_list', got {type(value).__name__}"
        )
    return OTELMetricAttributeFilter(
        include_list=value.get("include_list"),
        exclude_list=value.get("exclude_list"),
    )

