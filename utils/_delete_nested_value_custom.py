from typing import Any, Dict, List, Union

def _delete_nested_value_custom(
    data: Union[Dict[str, Any], List[Any]],
    segments: list,
    segment_index: int = 0,
) -> None:
    """
    Recursively delete a field from nested data using parsed segments.

    Modifies data in-place (caller must deep copy first).

    Args:
        data: Dictionary or list to modify
        segments: Parsed path segments
        segment_index: Current position in segments list
    """
    if segment_index >= len(segments):
        return

    segment = segments[segment_index]
    is_last = segment_index == len(segments) - 1

    # Handle array wildcard: [*]
    if segment == "[*]":
        if isinstance(data, list):
            for item in data:
                if is_last:
                    # Can't delete array elements themselves, skip
                    pass
                else:
                    # Only recurse if item is a dict or list (nested structure)
                    if isinstance(item, (dict, list)):
                        _delete_nested_value_custom(item, segments, segment_index + 1)
        return

    # Handle array index: [0], [1], [2], etc.
    if segment.startswith("[") and segment.endswith("]"):
        try:
            index = int(segment[1:-1])
            if isinstance(data, list) and 0 <= index < len(data):
                if is_last:
                    # Can't delete array elements themselves, skip
                    pass
                else:
                    # Only recurse if element is a dict or list (nested structure)
                    element = data[index]
                    if isinstance(element, (dict, list)):
                        _delete_nested_value_custom(
                            element, segments, segment_index + 1
                        )
        except (ValueError, IndexError):
            # Invalid index, skip
            pass
        return

    # Handle regular field navigation
    if isinstance(data, dict):
        if is_last:
            # Delete the field
            data.pop(segment, None)
        else:
            # Navigate deeper
            if segment in data:
                next_segment = (
                    segments[segment_index + 1]
                    if segment_index + 1 < len(segments)
                    else None
                )

                # If next segment is array notation, current field should be list
                if next_segment and (next_segment.startswith("[")):
                    if isinstance(data[segment], list):
                        _delete_nested_value_custom(
                            data[segment], segments, segment_index + 1
                        )
                # Otherwise navigate into dict
                elif isinstance(data[segment], dict):
                    _delete_nested_value_custom(
                        data[segment], segments, segment_index + 1
                    )

