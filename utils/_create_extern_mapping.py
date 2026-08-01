
def _create_extern_mapping(
    data: dict[str, Any],
) -> defaultdict[int, list[dict[str, Any]]]:
    """
    compute a mapping from external ids to non kernels, which contain the information we need to estimate flops etc
    """
    extern_mapping: defaultdict[int, list[dict[str, Any]]] = defaultdict(list)
    for event in data["traceEvents"]:
        if (
            "args" not in event
            or "External id" not in event["args"]
            or event["cat"] != "cpu_op"
        ):
            continue
        if len(extern_mapping[event["args"]["External id"]]) > 0:
            raise ParseException("duplicate external id in event")
        extern_mapping[event["args"]["External id"]].append(event)
    return extern_mapping

