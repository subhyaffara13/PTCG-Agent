from typing import List, Optional

def prometheus_label_factory(
    supported_enum_labels: List[str],
    enum_values: UserAPIKeyLabelValues,
    tag: Optional[str] = None,
    *,
    label_context: Optional[PrometheusLabelFactoryContext] = None,
) -> dict:
    """
    Returns a dictionary of label + values for prometheus.

    Ensures end_user param is not sent to prometheus if it is not supported.

    When ``label_context`` is provided, it must have been built from the same
    ``enum_values`` object; work is amortized (single model_dump, tag map, etc.).
    """
    if label_context is not None:
        if label_context.enum_values is not enum_values:
            raise ValueError(
                "label_context.enum_values must be the same object as enum_values"
            )
        return _prometheus_labels_from_context(supported_enum_labels, label_context)

    # Extract dictionary from Pydantic object
    enum_dict = enum_values.model_dump()

    # Filter supported labels and sanitize values to prevent breaking
    # the Prometheus text format (e.g. U+2028 Line Separator in label values)
    filtered_labels = {
        label: _sanitize_prometheus_label_value(value)
        for label, value in enum_dict.items()
        if label in supported_enum_labels
    }

    if UserAPIKeyLabelNames.END_USER.value in filtered_labels:
        get_end_user_id_for_cost_tracking = _get_cached_end_user_id_for_cost_tracking()

        filtered_labels["end_user"] = get_end_user_id_for_cost_tracking(
            litellm_params={"user_api_key_end_user_id": enum_values.end_user},
            service_type="prometheus",
        )

    if enum_values.custom_metadata_labels is not None:
        for key, value in enum_values.custom_metadata_labels.items():
            # check sanitized key
            sanitized_key = _sanitize_prometheus_label_name(key)
            if sanitized_key in supported_enum_labels:
                filtered_labels[sanitized_key] = _sanitize_prometheus_label_value(value)

    # Add custom tags if configured
    if enum_values.tags is not None:
        custom_tag_labels = get_custom_labels_from_tags(enum_values.tags)
        for key, value in custom_tag_labels.items():
            if key in supported_enum_labels:
                filtered_labels[key] = _sanitize_prometheus_label_value(value)

    for label in supported_enum_labels:
        if label not in filtered_labels:
            filtered_labels[label] = None

    return filtered_labels

