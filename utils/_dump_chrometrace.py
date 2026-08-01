
def _dump_chrometrace(schedule, filename):
    """
    This function dumps a schedule IR into a chrometrace format so it can be visualized.

    It is currently very basic and only serves as a graphical alternative to dumping the schedule IR as text.

    As future work we may extend this to include more accurate heuristics for durations, or let users input durations,
    add 'flow events' to let the UI show the connection between sends and recvs, and model cuda streams for comm/compute
    as separate streams on the chrometrace view.
    """
    events = []
    for rank in sorted(schedule):
        for timestep, action in enumerate(schedule[rank]):
            if action is None:
                continue
            events.append(
                {
                    "name": str(action),
                    "cat": (
                        "computation"
                        if action.computation_type in (F, B, W)
                        else "communication"
                    ),
                    "ph": "X",
                    "pid": rank,
                    "tid": rank,
                    "ts": timestep,
                    "dur": 1,
                }
            )
    import json

    with open(filename, "w") as f:
        json.dump({"traceEvents": events}, f)

