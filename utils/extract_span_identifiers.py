from typing import Any, Optional, Tuple

def extract_span_identifiers(
    current_span_data: Any,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract trace_id and parent_span_id from current_span_data.

    Args:
        current_span_data: Either dict with trace_id/id keys or Opik object

    Returns:
        Tuple of (trace_id, parent_span_id), both optional
    """
    if current_span_data is None:
        return None, None

    if isinstance(current_span_data, dict):
        return (current_span_data.get("trace_id"), current_span_data.get("id"))

    try:
        return current_span_data.trace_id, current_span_data.id
    except AttributeError:
        _logging.verbose_logger.warning(
            f"Unexpected current_span_data format: {type(current_span_data)}"
        )
        return None, None

