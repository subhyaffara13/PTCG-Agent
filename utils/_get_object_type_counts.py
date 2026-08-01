
def _get_object_type_counts(top_n: int) -> Tuple[int, List[Dict[str, Any]]]:
    """Count objects by type and return total count and top N types."""
    type_counts: Counter = Counter()
    total_objects = 0

    for obj in gc.get_objects():
        total_objects += 1
        obj_type = type(obj).__name__
        type_counts[obj_type] += 1

    top_object_types = [
        {"type": obj_type, "count": count, "count_readable": f"{count:,}"}
        for obj_type, count in type_counts.most_common(top_n)
    ]

    return total_objects, top_object_types

