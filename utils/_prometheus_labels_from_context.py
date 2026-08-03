from typing import Dict, List, Optional

def _prometheus_labels_from_context(
    supported_enum_labels: List[str],
    ctx: PrometheusLabelFactoryContext,
) -> Dict[str, Optional[str]]:
    filtered_labels: Dict[str, Optional[str]] = {
        label: ctx._sanitized_enum[label]
        for label in supported_enum_labels
        if label in ctx._sanitized_enum
    }

    if UserAPIKeyLabelNames.END_USER.value in filtered_labels:
        filtered_labels[UserAPIKeyLabelNames.END_USER.value] = (
            ctx.get_resolved_end_user()
        )

    for sk, val in ctx._custom_by_sanitized_key.items():
        if sk in supported_enum_labels:
            filtered_labels[sk] = val

    for k, v in ctx._tag_labels.items():
        if k in supported_enum_labels:
            filtered_labels[k] = v

    for label in supported_enum_labels:
        if label not in filtered_labels:
            filtered_labels[label] = None

    return filtered_labels

