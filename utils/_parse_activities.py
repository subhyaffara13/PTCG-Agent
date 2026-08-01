
def _parse_activities(
    activities: Iterable[ProfilerActivity | dict[ProfilerActivity, list[str]]],
) -> tuple[set[ProfilerActivity], dict[ProfilerActivity, set[str]]]:
    """Parse a mixed activities list into a set of activities and a filter dict.

    Each item is either a bare ``ProfilerActivity`` (collect all defaults) or a
    ``dict[ProfilerActivity, list[str]]`` (collect only the named subset).
    An empty list value (e.g. ``{CUDA: []}``) means collect nothing for that group.
    """
    parsed_activities: set[ProfilerActivity] = set()
    activity_filters: dict[ProfilerActivity, set[str]] = {}
    for item in activities:
        if isinstance(item, ProfilerActivity):
            if item in parsed_activities:
                raise ValueError(f"Activity {item} specified more than once")
            parsed_activities.add(item)
        elif isinstance(item, dict):
            for key, val in item.items():
                if key in parsed_activities:
                    raise ValueError(f"Activity {key} specified more than once")
                parsed_activities.add(key)
                activity_filters[key] = set(val)
        else:
            raise TypeError(f"Expected ProfilerActivity or dict, got {type(item)}")
    return parsed_activities, activity_filters

